-- insert values to publisher table with fake data, this is executed for 255 times 
-- this is also executed when the owner adding new books into the bookstore
INSERT INTO PUBLISHER VALUES ('National Academies Press','9899 Dixon Overpass North Pamela, PE E9T7N2','National_A@gmail.com','1-855-801-2519','4393827021637795',100001)

-- insert values to genre table with fake data, this is executed for 148 times 
-- this is also executed when the owner adding new books into the bookstore
INSERT INTO GENRE VALUES ('Business law',200001)

-- insert values to author table with fake data, this is executed for 654 times
-- this is also executed when the owner adding new books into the bookstore
INSERT INTO AUTHOR VALUES (300001,'Jane Wightwick')

-- insert values to book table with fake data, this is executed for 606 times
-- this is also executed when the owner adding new books into the bookstore
INSERT INTO BOOK VALUES ('Attack on Titan: Volume 13',43.28,192,'9781610000000',22,400001,100028,0.52)

-- insert values to customer table with fake data, this is executed for 498 times 
-- this is also executed when the user register in bookstore
insert into customer values (500001,'tjones','password')

-- insert values to payment_card table with fake data, this is executed for 3000 times 
-- this is also executed when the user checking out using new payment card
insert into payment_card values ('4055362012805732','378','09/25','George Miller','03908 Jeffrey Land Rebeccaport, BC M8J3G3','Master')

-- insert values to book_order table with fake data, this is executed for 3000 times
-- this is also executed when the user shopping at the bookstore and place order
insert into book_order values (600001,'DHL',500073,'George Miller','03908 Jeffrey Land Rebeccaport, BC M8J3G3','4055362012805732','Your order is in transit','2022-01-24')

-- insert values to contain table with fake data, this is executed for 5993 times
-- this is also executed when the user shopping at the bookstore and place order
insert into contain values (600001,400331,2)

-- insert values to utility table with fake data, this is executed for 12 times
-- this is also executed when the owner add the utility of the past month
insert into utility values (01,1582.89)


-- delete all the data in the tables, this is used when reinitializing the database
delete from publisher
delete from genre
delete from author
delete from book
delete from write
delete from typeof
delete from customer
delete from book_order
delete from contain
delete from utility
delete from SHOPPING_CART
delete from ORDER_FROM_PUBLISHER
delete from PAYMENT_CARD

-- this is executed when customer placing order on this book, the storage of this book is reduced
update book set storage = 20 where bid=400024

-- this is also executed when the owner update the utility of the past month
update utility set cost=1056.56 where month=12