-- execute the function check_book_storage() each time after new book_order placed and values are inserted in comtain table
CREATE TRIGGER ORDER_PLACE
    AFTER INSERT
    ON CONTAIN
    FOR EACH ROW
    EXECUTE PROCEDURE check_book_storage();

-- trigger function executed with trigger ORDER_PLACE
CREATE FUNCTION check_book_storage()
        returns TRIGGER
        language plpgsql
        AS
        $$
        -- save the amount of this book sold last month to variable _amount
        -- if there is no book sold last month, save 5 into the variable _amount
        DECLARE _amount int;
        begin 
        IF EXISTS (SELECT amount_sold_per_month.amount AS amount
            from amount_sold_per_month,(SELECT BOOK_ORDER.SDATE AS DATE FROM BOOK_ORDER WHERE BOOK_ORDER.OID = NEW.OID) AS SDATE
            where amount_sold_per_month.month = TO_CHAR(date_trunc('month', SDATE.DATE - interval '1' month), 'MM') AND amount_sold_per_month.bid = NEW.bid)
        THEN
            _amount := (SELECT amount_sold_per_month.amount 
            from amount_sold_per_month,(SELECT BOOK_ORDER.SDATE AS DATE FROM BOOK_ORDER WHERE BOOK_ORDER.OID = NEW.OID) AS SDATE
            where amount_sold_per_month.month = TO_CHAR(date_trunc('month', SDATE.DATE - interval '1' month), 'MM') AND amount_sold_per_month.bid = NEW.bid);
        ELSE
            _amount := 5;
        END IF;   

        -- check whether the storage of books is less than 20 after the order has been placed           
        IF (SELECT BOOK.STORAGE
            FROM BOOK
            WHERE BOOK.BID = NEW.BID) < 20

        --order from publisher by inserting the amount of this book sold last month, pid, bid, the order's date into ORDER_FROM_PUBLISHER table
        THEN
            --order from publisher
            WITH SDATE AS
            (SELECT BOOK_ORDER.SDATE AS DATE FROM BOOK_ORDER
            WHERE BOOK_ORDER.OID = NEW.OID)              
            INSERT INTO ORDER_FROM_PUBLISHER 
            SELECT 
                nextval('poidcreater'),
                amount_sold_per_month.amount,
                pid_table.pid,
                NEW.bid,
                SDATE.DATE 
            from amount_sold_per_month,(select pid from book where book.bid = new.bid) as pid_table, SDATE
            where amount_sold_per_month.month = TO_CHAR(date_trunc('month', SDATE.DATE - interval '1' month), 'MM') and
            amount_sold_per_month.bid = NEW.bid;
        
            -- update the storage of book by adding the amount of this book sold last month to the current book storage
            -- if there is no book sold last month, order 5 books instead        
            UPDATE BOOK SET STORAGE = storage + _amount WHERE BOOK.BID = NEW.BID;
        END IF;
               
        RETURN NEW;
        end;
        $$

