This program is written by python, the GUI is displayed by tkinter
The python version is 3.9.13

In order to run this program, please install the following packages:

1. psycopg2:    pip install psycopg2-binary
2. tkinter module:  pip install tk
3. openpyxl:    pip install openpyxl
4. faker:   pip install Faker
5. Python Standard Library 

The database is connected to an online PostgreSQL database: https://www.elephantsql.com/
The account username and password of this website is shown in the Appendix II part of the project report.
When running the program, please make sure your computer is connected to the internet in order to connect to the database

the dbinitializer.py creates the database using DDL and imports 606 books information download from online database, 255 fake publishers’ information, 500 fake customer and 3000 fake book orders by DML.

PLEASE NOTE：
You DON'T need to run dbinitializer.py unless you want to drop the database and re-import those fake data.
Running dbinitializer.py takes very long time(about 30 minutes) since it need to re-generate the fake data.


To use this desktop app please run the file app.py under python environment and install the packaegs listed.
If app.py runs successfully, you will see a tkinter app window showing on your screen, and "database connected" print put out the terminal.
In the admin login page, the admin username and password are both “admin”