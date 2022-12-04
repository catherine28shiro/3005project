-- executed when new element going to be inserted to corresponding table
select nextval('pidcreater')
select nextval('bidcreater')
select nextval('aidcreater')
select nextval('gidcreater')
select nextval('oidcreater')
select nextval('cidcreater')
select nextval('poidcreater')

-- get the pid of the publisher with given bid
-- used when adding books with the publisher's bid
select pid from publisher where name ='Burns Oates';

-- get the gid of the publisher with given genre type
-- used when mapping books with genre in the typeof table
select gid from genre where genre_type = 'Hatha yoga'

-- get the aid of the publisher with given name
-- used when mapping books with author in the write table
select aid from author where name = 'Jane Wightwick'

-- get the bill_name and address of the payment_card with card number
-- used adding new order, checking if the payment card already in the database
select payment_card.bill_name,payment_card.bill_address from payment_card where card_num='4055362012805732'

-- get the storage  of the book with bid
-- used customer adding book to shopping cart, checking if the storage is enough
select storage from book where bid=400045

-- get the information  of the customer with given username
-- used when user log in, checking if there is a user with this name, and if the password is correct
select * from customer where username='barryjared'

-- get the cid of the customer with given username
-- used when user registering, checking if the username is already exist
select cid from customer where username='barryjared'

-- get the cid of the book order with given oid
-- used when user searching oid and wants to view their order detail
select cid from book_order where oid=600003

-- get the info of the book with given ISBN
-- used when user searching book and owner deleting books (they need to search for the books they want to delete first)
select * from book where ISBN='9780770520000'



-- create a materialized view "ct" that joining book,write,typeof,genre,author,publisher tables, 
-- returning all book info,aid,author name,gid,genre_type,publisher name
-- used as the reference table when user searching books combining title, author, genre
CREATE MATERIALIZED VIEW ct 
AS select book.*,author.aid,author.name as Aname,genre.*,publisher.name as pname from book, write,typeof,genre,author,publisher
    where book.bid = write.bid and 
    book.bid = typeof.bid and 
    typeof.gid = genre.gid and 
    write.aid = author.aid and
    book.pid=publisher.pid

-- get the title of the book with the title contains the given word 'python' and genre contains word 'computer' 
-- and author name contain word 'ann' from materialized view ct
-- this is approximate search and case insensitive
-- used when user searching book, and owner deleting books (they need to search for the books they want to delete first)
select DISTINCT ct.title from ct
    where ct.title ilike 'python' and 
    ct.genre_type ilike 'computer' and 
    ct.Aname ilike 'ann';

-- get the all the information of the book,book's genre,author,publisher from materialized view ct
-- used when displaying book informating after user select the book they searched
select * from ct where title = 'A Divided World'

-- get the info from SHOPPING_CART with given cid and bid
-- used when adding books to shopping cart, checking if the customer has added this book to cart before
-- if used to add it, update the amount by add the new amount customer entered in book page
select * from SHOPPING_CART where cid=500003 and bid=400034

-- get the bid and amount from SHOPPING_CART with given cid 
-- used when displaying the books customer put in the shopping cart
select * from shopping_cart where cid =500003

-- get the title from materialized view ct with the bid get from the SHOPPING_CART
-- used when displaying the books customer put in the shopping cart
select ct.title from ct where ct.bid=400034

-- get the all th info from payment_card table with given card number
-- used when customer placing order, checking if the card is already stored in the database
select * from payment_card where card_num='9780770520000'

-- return book.title, oid, carrier, shipment status, amount by joining BOOK,BOOK_ORDER,CONTAIN table
-- this materialize table is created for viewing the detals for an order
CREATE MATERIALIZED VIEW book_in_order AS
    select book.title as title, book_order.oid as oid, book_order.carrier as carrier, book_order.SHIPMENT_STATUS as status, contain.amount as amount from BOOK,BOOK_ORDER,CONTAIN
    where book_order.oid = contain.oid and
    contain.bid = book.bid;

-- get the title,carrier,status,amount from materialize table book_in_order
-- used when customer searching their oid and goes to the OrderPage
select title,carrier,status,amount from book_in_order where oid=600001

-- get the oid from book_order with given cid
-- used when customer asking for their previous order number
select oid from book_order where cid =500003

-- get the info from publisher table with the given name, case insensitive 
-- used when owner adding new publisher, checking if the publisher name already exist
select * from publisher where name ILIKE 'university'

-- get the info from author table with the given name, case insensitive 
-- used when owner adding new author, checking if the author name already exist
select * from author where name ILIKE 'anny'

-- get the info from genre table with the given genre type, case insensitive 
-- used when owner adding new genre, checking if the genre already exist
select * from genre where genre_type ILIKE  'COMPUTER'

-- get the cost from utility table with the given month
-- used when owner adding or updating utility, checking if the cost already exits for that month
select cost from utility where month=%s

-- get the info from book table with the given title, case insensitive 
-- used when owner adding new book, checking if the book already exist
select * from book where title ILIKE %s


-- return publisher's name, publisher's email, book's title, book's ISBN, order_amount and order date of the bookstore ordering from bublishers by joining 
-- publisher, book, ORDER_FROM_PUBLISHER tables
-- this is used when displaying the pprevious order bookstore ordered from bublishers
CREATE MATERIALIZED VIEW book_order_record AS 
    select publisher.name as pname, publisher.email as pemail, book.title as title, 
    book.ISBN as ISBN, ORDER_FROM_PUBLISHER.order_amount as amount, ORDER_FROM_PUBLISHER.date as date
    from publisher, book, ORDER_FROM_PUBLISHER
    where publisher.pid = ORDER_FROM_PUBLISHER.pid and
    book.bid = ORDER_FROM_PUBLISHER.bid;

-- get all the info from materialized view book_order_record order by date in ascending order
-- this is used when displaying the pprevious order bookstore ordered from bublishers
select * from book_order_recoerd order by date asc


-- return the amount of sales for each author for each month 
-- by grouping the (joined tables contain, contain, book_order, write, book, author) by month and author name
-- used when displaying the report sales per author for each month 
CREATE MATERIALIZED VIEW sales_per_author AS 
    select author.name as name, sum(book.price) as price,TO_CHAR(book_order.sdate, 'MM') as month from contain, book_order, write, book, author
    where book.bid = write.bid and 
    author.aid = write.aid and
    book.bid = contain.bid and
    book_order.oid = contain.oid
    group by TO_CHAR(book_order.sdate, 'MM'),author.name
    order by name desc;

-- get the author name total price of the books(the sales) from  materialized view sales sales_per_author of the given month
-- used when displaying the report sales per author for the selected month 
select name,price from sales_per_author where month=%s order by price desc


-- return the amount of sales for each genre for each month 
-- by grouping the (joined tables contain, book_order, genre, book, TYPEOF) by month and genre type
-- used when displaying the report sales per genre for each month 
CREATE MATERIALIZED VIEW sales_per_genre AS 
    select TO_CHAR(book_order.sdate, 'MM') as month, genre.genre_type as type, sum(book.price) as price from contain, book_order, genre, book, TYPEOF
    where book.bid = typeof.bid and 
    genre.gid = typeof.gid and
    book.bid = contain.bid and
    book_order.oid = contain.oid
    group by TO_CHAR(book_order.sdate, 'MM'), genre.genre_type 
    order by type desc;

-- get the genre type, total price of the books(the sales) from materialized view sales_per_genre of the given month
-- used when displaying the report sales per genre type for the selected month 
select type,price from sales_per_genre where month=%s order by price desc


-- return the amount of sales and the corresponding month for each publisher for each month
-- used when displaying the report sales per publisher for each month and used for the creation of materialized view expenditure
CREATE MATERIALIZED VIEW sales_to_publisher AS 
    select pname, sum(sales) as sale, TO_CHAR(sdate, 'MM') as month from
    (select publisher.name as pname, publisher.BANK_ACC as pbank, (book.SALESPERCENT_TO_PUB * book.price) as sales, book_order.sdate as sdate
    from contain, book_order, book, publisher
    where book.bid = contain.bid and
    book_order.oid = contain.oid and
    book.pid = publisher.pid)sales_table
    group by pname, TO_CHAR(sdate, 'MM')
    order by pname desc;

-- get the publisher name, sales amount, publisher bank account from sales_to_publisher and publisher for the given month in decending order
-- used when displaying the report sales per publisher for the selected month
select pname,sale, publisher.BANK_ACC  
        from sales_to_publisher, publisher
        where month=%s and sales_to_publisher.pname = publisher.name order by sale desc

-- return the expenditure (utility + money transfered to publisher) for each month 
-- used when creating the materialized view sales_vs_expenditure
CREATE MATERIALIZED VIEW expenditure AS 
    select (utility.cost + pay_pub) as expen, utility.month as month, pay_pub, utility.cost as utility
    from utility, (select sum(sales_to_publisher.sale) as pay_pub, sales_to_publisher.month as pmonth
    from sales_to_publisher
    group by sales_to_publisher.month) pay_pub_table
    where utility.month = pmonth
    order by month asc;

-- return the expenditure, utility, payment to publisher, sales, profit of the bookstore for each month 
-- used when displaying the report sales_vs_expenditure
CREATE MATERIALIZED VIEW sales_vs_expenditure AS 
    select expen, utility, pay_pub, sales, (sales - expen) as profit, sale_table.month as month from
    expenditure, 
    (select sum(book.price) as sales, TO_CHAR(book_order.sdate, 'MM') as month from
    book, book_order,contain
    where book.bid= contain.bid and 
    book_order.oid = contain.oid
    group by TO_CHAR(book_order.sdate, 'MM')) sale_table
    where sale_table.month = expenditure.month;


-- get the month,sales,expenditure, profit,utility,payment to publisher from materialized view sales_vs_expenditure of the given month
-- used when displaying the report sales_vs_expenditure for the selected month 
select month,sales,expen, profit,utility,pay_pub from sales_vs_expenditure where month=%s


-- return the amount of each book sold per month
-- used in trigger function ordering amount of books sold last month from publisher
CREATE MATERIALIZED VIEW amount_sold_per_month AS 
    select bid, sum(sales) as amount, TO_CHAR(sdate, 'MM') as month from
    (select book.bid as bid, 1 as sales, book_order.sdate as sdate                                                                                                                                                                                                                              
    from contain, book_order, book
    where book.bid = contain.bid and
    book_order.oid = contain.oid)sales_table
    group by bid, TO_CHAR(sdate, 'MM')
    order by month asc;


-- refresh the materialized views
-- used when new orders created or books added or deleted or the the owner want to review the report
REFRESH MATERIALIZED VIEW ct;
REFRESH MATERIALIZED VIEW book_in_order;
REFRESH MATERIALIZED VIEW sales_per_author;
REFRESH MATERIALIZED VIEW sales_per_genre;
REFRESH MATERIALIZED VIEW sales_to_publisher;
REFRESH MATERIALIZED VIEW expenditure;
REFRESH MATERIALIZED VIEW sales_vs_expenditure;
REFRESH MATERIALIZED VIEW amount_sold_per_month;
REFRESH MATERIALIZED VIEW book_order_record;

-- DROP the materialized views
-- used when reinitialized the database
DROP MATERIALIZED VIEW ct;
DROP MATERIALIZED VIEW book_in_order;
DROP MATERIALIZED VIEW sales_per_author;
DROP MATERIALIZED VIEW sales_per_genre;
DROP MATERIALIZED VIEW sales_to_publisher;
DROP MATERIALIZED VIEW expenditure;
DROP MATERIALIZED VIEW sales_vs_expenditure;
DROP MATERIALIZED VIEW amount_sold_per_month;
DROP MATERIALIZED VIEW book_order_record;
    