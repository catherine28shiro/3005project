-- create utility table
create table IF NOT EXISTS UTILITY
    (MONTH          varchar(2)      NOT NULL UNIQUE,
    COST            numeric(8,2)    NOT NULL,        
    primary key (MONTH)
    );

-- create publisher table
create table IF NOT EXISTS PUBLISHER
    (NAME           varchar(60)     NOT NULL UNIQUE,
    ADDRESS         varchar(100),
    EMAIL           varchar(100),
    PHONE           varchar(20),
    BANK_ACC        varchar(50),
    PID             int             NOT NULL UNIQUE,
    primary key (PID)
    );
 
-- create book table
create table IF NOT EXISTS BOOK
    (TITLE		            varchar(300)	NOT NULL,		
    PRICE		            numeric(7,2)	NOT NULL,
    PAGE_COUNT	            int             NOT NULL,
    ISBN	                varchar(13)     UNIQUE NOT NULL,
    STORAGE		            int             NOT NULL,
    BID                     int             UNIQUE NOT NULL,
    PID                     int,
    SALESPERCENT_TO_PUB     numeric(3,2)    NOT NULL,
    primary key (BID),
    foreign key (PID) references PUBLISHER (PID) ON DELETE CASCADE
);

-- create genre table
create table IF NOT EXISTS GENRE
    (genre_type     varchar(30) NOT NULL UNIQUE,
    GID             int         NOT NULL UNIQUE,
    primary key (GID)
);

-- create typeof table, mapping book and genre
create table IF NOT EXISTS TYPEOF
    (GID    int     NOT NULL,
    BID     int     NOT NULL,
    primary key (BID,GID),
    foreign key (GID) references GENRE (GID) ON DELETE CASCADE,
    foreign key (BID) references BOOK (BID) ON DELETE CASCADE
    );

-- create author table
create table IF NOT EXISTS AUTHOR
    (AID    int         NOT NULL UNIQUE,
    NAME    varchar(50) NOT NULL,
    primary key (AID)
);

-- create write table, mapping author and book
create table IF NOT EXISTS WRITE
    (AID    int         NOT NULL,
    BID     int         NOT NULL,
    primary key (BID,AID),
    foreign key (AID) references AUTHOR (AID) ON DELETE CASCADE,
    foreign key (BID) references BOOK (BID) ON DELETE CASCADE
);

-- create customer table
create table IF NOT EXISTS CUSTOMER
    (CID            int         NOT NULL UNIQUE,
    USERNAME        varchar(50) NOT NULL UNIQUE,
    PASSWORD        varchar(15) NOT NULL,  
    primary key (CID)  
);

-- create shopping_cart table
create table IF NOT EXISTS SHOPPING_CART
    (CID            int         NOT NULL,  
    BID             int         NOT NULL,
    amount          int         NOT NULL,
    primary key (CID,BID),
    foreign key (BID) references BOOK (BID) ON DELETE CASCADE
);

-- create payment_card table
create table IF NOT EXISTS PAYMENT_CARD
    (CARD_NUM        varchar(16)    UNIQUE NOT NULL,
    CVV             varchar(3)      NOT NULL,
    EXP_DATE        varchar(5)      NOT NULL,
    BILL_NAME       varchar(50)     NOT NULL,
    BILL_ADDRESS    varchar(100)    NOT NULL,
    PAYMENT_TYPE    varchar(10)     NOT NULL,
    primary key (CARD_NUM)
);

-- create book_order table
create table IF NOT EXISTS BOOK_ORDER
    (OID            int         NOT NULL,
    CARRIER         varchar(30),
    CID             int         NOT NULL, 
    SHIP_NAME       varchar(50),
    SHIP_ADDRESS    varchar(100),
    CARD_NUM        varchar(16),
    SHIPMENT_STATUS varchar(70),
    SDATE           DATE,
    primary key (OID),
    foreign key (CID) references CUSTOMER (CID) ON DELETE CASCADE,
    foreign key (CARD_NUM) references PAYMENT_CARD (CARD_NUM) ON DELETE CASCADE   
);

-- create contain table, mapping book and oid
create table IF NOT EXISTS CONTAIN
    (OID            int         NOT NULL,
    BID             int         NOT NULL,
    AMOUNT          int         NOT NULL,
    primary key (OID,BID),
    foreign key (BID) references BOOK (BID) ON DELETE CASCADE,
    foreign key (OID) references BOOK_ORDER (OID) ON DELETE CASCADE
);

-- create order_from_publisher table, recording the ordered placed by the owner with publisher when book storage<20
create table IF NOT EXISTS ORDER_FROM_PUBLISHER
    (PUB_ORDER_ID   int             NOT NULL UNIQUE,
    ORDER_AMOUNT    int             NOT NULL,
    PID             int             NOT NULL,
    BID             int             NOT NULL,       
    DATE            DATE            NOT NULL,     
    primary key (PUB_ORDER_ID),
    foreign key (BID) references BOOK (BID) ON DELETE CASCADE,
    foreign key (PID) references PUBLISHER (PID) ON DELETE CASCADE
);

-- drop the tables, used when re-initializing the database
drop table IF EXISTS PUBLISHER CASCADE
drop table IF EXISTS BOOK CASCADE
drop table IF EXISTS AUTHOR CASCADE
drop table IF EXISTS GENRE CASCADE
drop table IF EXISTS TYPEOF CASCADE
drop table IF EXISTS WRITE CASCADE
drop table IF EXISTS BOOK_ORDER CASCADE
drop table IF EXISTS CUSTOMER CASCADE
drop table IF EXISTS CONTAIN CASCADE
drop table IF EXISTS SHOPPING_CART CASCADE
drop table IF EXISTS UTILITY CASCADE
drop table IF EXISTS PAYMENT_CARD CASCADE
drop table IF EXISTS ORDER_FROM_PUBLISHER CASCADE

-- create the sequnce used for pid oid cid bid aid gid poid, automatically add one when inserting new elements
CREATE SEQUENCE pidcreater
AS BIGINT
INCREMENT BY 1
MINVALUE 100001
NO MAXVALUE;

CREATE SEQUENCE gidcreater
AS BIGINT
INCREMENT BY 1
MINVALUE 200001
NO MAXVALUE;

CREATE SEQUENCE aidcreater
AS BIGINT
INCREMENT BY 1
MINVALUE 300001
NO MAXVALUE;

CREATE SEQUENCE bidcreater
AS BIGINT
INCREMENT BY 1
MINVALUE 400001
NO MAXVALUE;

CREATE SEQUENCE cidcreater
AS BIGINT
INCREMENT BY 1
MINVALUE 500001
NO MAXVALUE;

CREATE SEQUENCE oidcreater
AS BIGINT
INCREMENT BY 1
MINVALUE 600001
NO MAXVALUE;

CREATE SEQUENCE poidcreater
AS BIGINT
INCREMENT BY 1
MINVALUE 700001
NO MAXVALUE;

-- drop the sequence for the above ids, used when reinitializing the database
DROP SEQUENCE IF EXISTS pidcreater CASCADE;
DROP SEQUENCE IF EXISTS gidcreater CASCADE;
DROP SEQUENCE IF EXISTS aidcreater CASCADE;
DROP SEQUENCE IF EXISTS bidcreater CASCADE;
DROP SEQUENCE IF EXISTS cidcreater CASCADE;
DROP SEQUENCE IF EXISTS oidcreater CASCADE;
DROP SEQUENCE IF EXISTS poidcreater CASCADE;