# STUDENT ID:101209708
# NAME: Catherine Li

from tkinter import *
from tkinter import messagebox
import tkinter.font as TkFont
from random import randint
import psycopg2
from datetime import date

hostname = 'peanut.db.elephantsql.com'
database = 'iogkcxzz'
username='iogkcxzz'
pwd='4BgZjz6v_2N1448Ftv1TQGLR5VKKT1ab'

adminUsername = 'admin'
adminPassword = 'admin'

# refresh materialed views
def refreshMaterializeView():
    cur.execute('REFRESH MATERIALIZED VIEW ct;')
    cur.execute('REFRESH MATERIALIZED VIEW book_in_order;')
    cur.execute('REFRESH MATERIALIZED VIEW sales_per_author;')
    cur.execute('REFRESH MATERIALIZED VIEW sales_per_genre;')
    cur.execute('REFRESH MATERIALIZED VIEW sales_to_publisher;')
    cur.execute('REFRESH MATERIALIZED VIEW expenditure;')
    cur.execute('REFRESH MATERIALIZED VIEW sales_vs_expenditure;')
    cur.execute('REFRESH MATERIALIZED VIEW amount_sold_per_month;')
    cur.execute('REFRESH MATERIALIZED VIEW book_order_record;')

##########################################
#   the main app controller              #
##########################################
class BookStoreAppGUI(Tk):
    # initialize the GUI class
    def __init__(self):
        # initialize the Tk
        Tk.__init__(self)
        # set font her
        self.font = TkFont.Font(family="Helvetica", size="16",weight='bold')
        self.Tfont = TkFont.Font(family="Helvetica", size="14")
        self.selectedBook = ''
        self.LOGIN = False
        #current logged in customer id
        self.cid=0000
        #books in shopping cart
        self.cart=[]
        #current order number customer is searching
        self.oid=0000

        # The big container containers all the frames
        container = Frame()
        container.grid(row=0,column=0)

        # the list containing all the frames
        self.frame_list={}

        # the month of report admin want to see
        self.month=''

        # the type of report admin want to see
        self.report=''

        # create all the frames from each page class CartPage,BookPage,CheckoutPage,\
        #     OrderPage,TrackPage,AdminPage,ReportPage,AdminLoginPage
        for page in (CartPage,FirstPage,AdminLoginPage,UserLoginPage,BookPage,UserRegPage,CheckoutPage,OrderPage,\
            GetOrderNumberPage,adminFirstPage,adminSecondPage,reportFirstPage,reportSecondPage,reportThirdPage,OrderfromPubPage):
            name = page.__name__
            frame = page(parent=container,controller=self)
            frame.grid(row=0,column=0,sticky="nsew")
            self.frame_list[name] = frame

        # show first page at the beginning  
        self.switch_frame('FirstPage')

    # switch between frames
    def switch_frame(self,name):
        page = self.frame_list[name]
        page.tkraise()
        if name == 'BookPage' or name=='CartPage' or name =='CheckoutPage' or name=='OrderPage' or name=='GetOrderNumberPage' or name=='reportThirdPage' or name=='OrderfromPubPage':
            page.refresh()

##########################################
#   login and register pages             #
##########################################

# admin login page
class AdminLoginPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        # back to home page
        Button(self,text ='Back to Home', font=controller.font,command=lambda: controller.switch_frame('FirstPage'))\
        .place(relx=.5, rely=.2,anchor= CENTER)

        # Admin name
        self.adminname=StringVar()
        Label(self,text ='Admin Name: ', font=controller.font,pady=50).place(relx=.38, rely=.5,anchor= CENTER)
        self.name_entry = Entry(self,textvariable=self.adminname, width=30)
        self.name_entry.place(relx=.6, rely=.5,anchor= CENTER)
        # Admin Password
        self.adminpsw=StringVar()
        Label(self,text ='Admin Password: ',font=controller.font).place(relx=.35, rely=.6,anchor= CENTER)
        self.psw_entry=Entry(self,textvariable=self.adminpsw,width=30)
        self.psw_entry.place(relx=.6, rely=.6,anchor= CENTER)
        # Login button
        Button(self,text ='Log in', font=controller.font,command=lambda:self.adminLogin()).place(relx=.52, rely=.8,anchor= CENTER)
    def adminLogin(self):
        if self.adminname.get() != adminUsername or self.adminpsw.get()!=adminPassword:          
            messagebox.showerror("Error","Wrong admin name or password!")
        else:
            self.controller.switch_frame('adminFirstPage')
        self.psw_entry.delete(0,END)
        self.name_entry.delete(0,END)

# user login page
class UserLoginPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        # back to home page
        Button(self,text ='Back to Home', font=controller.font,command=lambda: controller.switch_frame('FirstPage'))\
        .place(relx=.5, rely=.2,anchor= CENTER)

        # User name
        self.username=StringVar()
        Label(self,text ='User Name: ', font=controller.font,pady=50).place(relx=.38, rely=.5,anchor= CENTER)
        self.username_entry=Entry(self,textvariable=self.username, width=30)
        self.username_entry.place(relx=.6, rely=.5,anchor= CENTER)
        # User Password
        self.psw=StringVar()
        Label(self,text ='User Password: ',font=controller.font).place(relx=.35, rely=.6,anchor= CENTER)
        self.psw_entry=Entry(self,textvariable=self.psw,width=30)
        self.psw_entry.place(relx=.6, rely=.6,anchor= CENTER)
        # Login button
        Button(self,text ='Log in', font=controller.font,command=lambda:self.userLogin()).place(relx=.52, rely=.8,anchor= CENTER)
    
    def userLogin(self):
        username = self.username.get()
        psw = self.psw.get()
        cur.execute('select * from customer where username=%s',(username,))
        customer = cur.fetchall()
        self.username_entry.delete(0, END)
        self.psw_entry.delete(0, END)
        if customer:
            if(customer[0][2] != psw):
                messagebox.showerror("Error","Wrong password!")
            else:
                self.controller.LOGIN = True
                self.controller.cid = customer[0][0]
                messagebox.showinfo("Success","You have logged in!")
                self.controller.switch_frame('FirstPage')

        else:
            messagebox.showerror("Error","No such username, Please try again")

# user registration page
class UserRegPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
         # back to home page
        Home_btn=Button(self,text ='Back to Home', font=controller.font,command=lambda: controller.switch_frame('FirstPage'))\
        .place(relx=.5, rely=.2,anchor= CENTER)

        # User name
        self.username=StringVar()
        name_label=Label(self,text ='User Name: ', font=controller.font,pady=50).place(relx=.38, rely=.5,anchor= CENTER)
        self.name_entry=Entry(self,textvariable=self.username, width=30)
        self.name_entry.place(relx=.6, rely=.5,anchor= CENTER)
        # User Password
        self.password = StringVar()
        psw_label=Label(self,text ='User Password: ',font=controller.font).place(relx=.35, rely=.6,anchor= CENTER)
        self.psw_entry=Entry(self,textvariable=self.password,width=30)
        self.psw_entry.place(relx=.6, rely=.6,anchor= CENTER)
        # Register button
        Login_btn=Button(self,text ='Register', font=controller.font,command=lambda:self.register()).place(relx=.52, rely=.8,anchor= CENTER)

    def register(self):
        username = self.username.get()
        cur.execute('select cid from customer where username=%s',(username,))
        if cur.fetchall():
            messagebox.showerror("Invalid username","Duplicate username, please try another username!")
        else:
            cur.execute("select nextval('cidcreater')")
            cid = cur.fetchall()[0][0]
            cur.execute("insert into customer values (%s,%s,%s)",(cid,username,self.password.get()))
            conn.commit()
            messagebox.showinfo("success","You have registered in our book store!")
            self.name_entry.delete(0, END)
            self.psw_entry.delete(0, END)
            self.controller.switch_frame('FirstPage')


##########################################
#   the home page of the app             #
##########################################   
class FirstPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        # controller help children page get properties from the big frame
        self.controller=controller
        self.content(controller)

    def logout(self):
        if not self.controller.LOGIN:
            messagebox.showerror("Error","You have not logged in")
        else:
            self.controller.LOGIN = False
            self.controller.cid=0000
            messagebox.showinfo("Success","You have logged out")
        
    def login(self):
        if self.controller.LOGIN:
            messagebox.showerror("Error","You have already logged in!")
        else:
            self.controller.switch_frame('UserLoginPage')
    def gotoCart(self):
        if not self.controller.LOGIN:
            messagebox.showerror("Error","Please login first!")
        else:
            self.controller.switch_frame('CartPage')
    def searchOrder(self,oid):
        if not oid:
            messagebox.showerror("Error","Please enter a number!")
        if not self.controller.LOGIN:
            messagebox.showerror("Error","Please log in!")
        else:
            self.controller.oid = int(oid)
            cur.execute('select cid from book_order where oid=%s',(oid,))
            if cur.fetchall():
                self.controller.switch_frame('OrderPage')
            else:
                messagebox.showerror("Error","No such order, please try other order numbers!")
    def gotoOrderNum(self):
        if not self.controller.LOGIN:
            messagebox.showerror("Error","Please log in!")
        else:
            self.order_entry.delete(0,END)
            self.controller.switch_frame('GetOrderNumberPage')
    def content(self,controller):
        #nevigator part
        left_frame = Frame(self)
        left_frame.grid(row=0, column=0, sticky="nswe")
        Adminlogin_btn=Button(left_frame,text ='Admin Login', font=controller.font,command=lambda: controller.switch_frame('AdminLoginPage'),width=12)
        Adminlogin_btn.grid(row=0,column=0,pady=30,padx=20,sticky=W)
        Userlogin_btn=Button(left_frame,text ='User Login', font=controller.font,command=lambda: self.login(),width=12)
        Userlogin_btn.grid(row=1,column=0,pady=30,sticky=W,padx=20)
        UserReg_btn=Button(left_frame,text ='User Register', font=controller.font,command=lambda: controller.switch_frame('UserRegPage'),width=12)
        UserReg_btn.grid(row=2,column=0,pady=30,sticky=W,padx=20)
        UserLogout_btn=Button(left_frame,text ='User Logout', font=controller.font,command=lambda: self.logout(),width=12)
        UserLogout_btn.grid(row=3,column=0,pady=30,sticky=W,padx=20)
        Cart_btn=Button(left_frame,text ='Shopping Cart', font=controller.font,command=lambda: self.gotoCart(),width=12)
        Cart_btn.grid(row=4,column=0,pady=30,sticky=W,padx=20)
        Order_btn=Button(left_frame,text ='View Order Numbers', font=controller.font,command=lambda: self.gotoOrderNum(),wraplength=160,width=12)
        Order_btn.grid(row=5,column=0,pady=30,sticky=W,padx=20)
        

        # main part
        right_frame = Frame(self)
        right_frame.grid(row=0, column=1, sticky="nswe")
        # Search for order
        oid_text=StringVar()
        order_label=Label(right_frame,text ='Order number: ', font=controller.Tfont,pady=20,wraplength=70)
        order_label.grid(row=0,column=0)
        self.order_entry=Entry(right_frame,textvariable=oid_text, width=40)
        self.order_entry.grid(sticky=W,row=0,column=1)
        search_btn = Button(right_frame,text ="Search",font=controller.Tfont,width=12,command=lambda: self.searchOrder(oid_text.get()))
        search_btn.grid(row=0,column=2,padx=30)
        # slogan
        slogan_label=Label(right_frame,text ='Search your book!', font=TkFont.Font(family="Helvetica", size="25",weight='bold'),pady=10)
        slogan_label.grid(row=1,column=1)
        # book information
        title_text=StringVar()
        book_label=Label(right_frame,text ='Book Name: ', font=controller.Tfont,pady=20)
        book_label.grid(row=2,column=0)
        self.book_entry=Entry(right_frame,textvariable=title_text, width=40)
        self.book_entry.grid(sticky=W,row=2,column=1)
        # author information
        author_text=StringVar()
        author_label=Label(right_frame,text ='Author Name: ',font=controller.Tfont)
        author_label.grid(row=2,column=2)
        self.author_entry=Entry(right_frame,textvariable=author_text,width=40)
        self.author_entry.grid(sticky=W,row=2,column=3)
        # ISBN information
        ISBN_text=StringVar()
        ISBN_label=Label(right_frame,text ='ISBN: ', font=controller.Tfont)
        ISBN_label.grid(row=3,column=0)
        self.ISBN_entry=Entry(right_frame,textvariable=ISBN_text,width=40)
        self.ISBN_entry.grid(sticky=W,row=3,column=1)
        # genre information
        genre_text=StringVar()
        genre_label=Label(right_frame,text ='Genre: ', font=controller.Tfont)
        genre_label.grid(row=3,column=2)
        self.genre_entry=Entry(right_frame,textvariable=genre_text, width=40)
        self.genre_entry.grid(sticky=W,row=3,column=3)

        #search button
        search_btn = Button(right_frame,text ="Search",font=controller.Tfont,width=12,\
            command=lambda: self.searchBook(title_text.get(),author_text.get(),ISBN_text.get(),genre_text.get()))
        search_btn.grid(sticky=W,row=4,column=1,pady=20)
        
        frame  = Frame(right_frame)
        frame.grid(row=5,column=1,rowspan=4,columnspan=4,sticky=W)
        #scroll bar
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT,fill=Y)
        #search result
        self.result = Listbox(frame,height=15,width=100,yscrollcommand=scrollbar.set)
        self.result.pack(side=LEFT,fill=Y)
        scrollbar.configure(command=self.result.yview)
    
        
        detail_btn = Button(right_frame,text="See Details",font=controller.Tfont,width=12,command=lambda: self.getSelected(controller))
        detail_btn.grid(sticky=W,row=10,column=1,pady=20)

    def searchBook(self,title,author,ISBN,genre):
        # clean the list box first   
        self.result.delete(0,END)

        if ISBN != "":
            cur.execute('select * from book where ISBN = %s',(ISBN,))
            for book in cur.fetchall():
                self.result.insert(END,book[0])
            return

        cur.execute('''select DISTINCT ct.title from ct
                    where ct.title ilike %s and 
                    ct.genre_type ilike %s and 
                    ct.Aname ilike %s''',('%'+title+'%','%'+genre+'%','%'+author+'%'))
        for book in cur.fetchall():
                self.result.insert(END,book[0])
        return
        
    def getSelected(self,controller):
        values = self.result.curselection()
        if  values:
            controller.selectedBook = self.result.get(values[0])
            self.result.delete(0,END)
            self.author_entry.delete(0,END)
            self.book_entry.delete(0,END)
            self.genre_entry.delete(0,END)
            self.ISBN_entry.delete(0,END)
            controller.switch_frame('BookPage')
        else:
            messagebox.showwarning("book not selected", "Warning:Please select a book!")


##########################################################################################################
#   Pages for customer: the book detail page, shopping cart page and place order page, view order page   #
##########################################################################################################   
# book detail page for customer
class BookPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        var = StringVar()
        pageLabel = Label(self,textvariable=var,font=("Helvetica", 20),pady=20, wraplength=600)
        var.set(self.controller.selectedBook)
        pageLabel.pack()    

        cur.execute('select * from ct where title = %s',(self.controller.selectedBook,))
        book = cur.fetchall()
        self.bid = book[0][5]
        self.storage = book[0][4]
        genres = ''
        authors=''
        for i in range(len(book)):
            if book[i][10] not in genres:
                if i != 0:
                    genres+=' ,'
                genres+= book[i][10]            
            if book[i][9] not in authors:
                if i != 0:
                    authors+=' ,'
                authors+=book[i][9]                         
        Label(self,text='Author: '+authors,font=self.controller.Tfont,pady=10,wraplengt=600).pack() 
        Label(self,text='Genre: '+genres,font=self.controller.Tfont,pady=10,wraplengt=600).pack()
        publisher = book[0][12]
        Label(self,text='Publisher: '+publisher,font=self.controller.Tfont,pady=10).pack() 
        Label(self,text='Number of Pages: '+str(book[0][2]),font=self.controller.Tfont,pady=10).pack()
        Label(self,text='ISBN: '+book[0][3],font=self.controller.Tfont,pady=10).pack() 
        Label(self,text='Price: $'+str(book[0][1]),font=self.controller.Tfont,pady=10).pack()

        frame = Frame(self)
        frame.pack()
        Button(frame,text ='Back to search page', font=self.controller.font,\
            command=lambda: self.controller.switch_frame('FirstPage')).grid(column=2,row=0,pady=20)
        Label(frame,text ='Please enter amount: ', font=self.controller.Tfont,pady=20).grid(column=2,row=1,pady=20)
        self.amount = StringVar()
        Entry(frame,textvariable=self.amount,width=10).grid(sticky=W,column=3,row=1,)
        Button(frame,text ='Add to Shopping Cart', font=self.controller.font,\
            command=lambda: self.addtoCart()).grid(column=2,row=2)
       
    def addtoCart(self):
        if not self.controller.LOGIN:
            messagebox.showerror("Error","Please log in first!")
            self.controller.switch_frame('UserLoginPage')
        else:
            cid = self.controller.cid
            # checking if the customer has added this book to cart before if used to add it, update the amount by add the new amount customer entered in book page
            cur.execute('select * from SHOPPING_CART where cid=%s and bid=%s',(cid,self.bid))
            bookInCart = cur.fetchall()
            if bookInCart:
                amount = bookInCart[0][2]
                number = int(self.amount.get()) + amount
                if number > self.storage:
                    messagebox.showerror("Error","The amount you entered exceed our storage!")
                else:
                    cur.execute('UPDATE SHOPPING_CART SET amount=%s where cid=%s and bid=%s',(number,cid,self.bid))
                    messagebox.showinfo("Success","You have added this book to shopping cart!")
                    conn.commit()
            # customer has never been added this book to cart:
            else:
                if self.amount.get() == '':
                    messagebox.showerror("Error","Please enter the amount you want!")
                else:
                    if int(self.amount.get()) > self.storage:
                        messagebox.showerror("Error","The amount you entered exceed our storage!")
                    else:
                        cur.execute("insert into SHOPPING_CART values (%s,%s,%s)",(cid,self.bid,int(self.amount.get())))
                        conn.commit()
                        messagebox.showinfo("Success","You have added this book to shopping cart!")

# shopping cart page for customer
class CartPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        # controller help children page get properties from the big frame
        self.controller=controller

    def refresh(self):
        Button(self,text="Go back to home page",font=self.controller.font,command=lambda: \
            self.controller.switch_frame('FirstPage')).grid(row=0,column=3,pady=20)
        Button(self,text="clear shopping cart",font=self.controller.font,command=lambda: self.delete(books)).grid(row=0,column=2,padx=20)
        Label(self,text="These are the books in your shopping cart:",font=("Helvetica", 20),pady=20).grid(row=1,column=2,padx=20)
        cur.execute('select * from shopping_cart where cid =%s',(self.controller.cid,))
        books = cur.fetchall()
        self.controller.cart = books
        frame  = Frame(self)
        frame.grid(row=2,column=1,rowspan=4,columnspan=4)
        #scroll bar
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT,fill=Y)
        #search result
        self.result = Listbox(frame,height=20,width=100,yscrollcommand=scrollbar.set)
        self.result.pack(side=LEFT,fill=Y)
        scrollbar.configure(command=self.result.yview)
        for b in books:
            cur.execute('select ct.title from ct where ct.bid=%s',(b[1],))
            title = cur.fetchall()[0][0]
            self.result.insert(END,'Title: '+title+'   Amount: '+str(b[2]))

        Button(self,text="Check out",font=self.controller.font,command=lambda:self.checkout()).grid(row=7,column=2,pady=20)

    def checkout(self):
        if not self.controller.cart:
            messagebox.showerror("error","There are no books in your shopping cart!")
        else:
            self.controller.switch_frame('CheckoutPage')

    def delete(self,books):
        if books:
            for b in books:
                cur.execute("delete from shopping_cart where bid = %s",(b[1],))
            conn.commit()
            self.result.delete(0,END)
            self.controller.switch_frame('CartPage')
        else:
            messagebox.showerror("Error","you have no books in shopping cart!")

# place order page for customer
class CheckoutPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller

    def refresh(self):
        Label(self,text ='Checking Out...', font=TkFont.Font(family="Helvetica", size="20")).grid(row=0,column=1,pady=20,padx=20)
        #billing name and address
        billname = StringVar()
        Label(self,text ='Billing name: ', font=self.controller.Tfont).grid(row=1,column=1,padx=10)
        Entry(self,textvariable=billname, width=50).grid(row=1,column=3,pady=10,sticky=W)
        billaddress = StringVar()
        Label(self,text ='Billing address: ', font=self.controller.Tfont).grid(row=2,column=1,padx=10)
        Entry(self,textvariable=billaddress, width=100).grid(row=2,column=3,pady=10,sticky=W)
        
        shipname = StringVar()
        Label(self,text ='Shipping name: ', font=self.controller.Tfont).grid(row=3,column=1,padx=10)
        Entry(self,textvariable=shipname, width=50).grid(row=3,column=3,pady=10,sticky=W)
        shipaddress = StringVar()
        Label(self,text ='Shipping address: ', font=self.controller.Tfont).grid(row=4,column=1,padx=10)
        Entry(self,textvariable=shipaddress, width=100).grid(row=4,column=3,pady=10,sticky=W)
        OPTIONS = ['Visa','Master']
        creditCard = StringVar()
        creditCard.set(OPTIONS[0])
        OptionMenu(self, creditCard, *OPTIONS).grid(row=5,column=1,pady=10)
        
        expDate=StringVar()
        Label(self,text ='Expire Date(mm/yr): ', font=self.controller.Tfont).grid(row=6,column=1,padx=10)
        Entry(self,textvariable=expDate,width=10).grid(row=6,column=3,pady=10,sticky=W)
        cvv=StringVar()
        Label(self,text ='CVV(3 digits): ', font=self.controller.Tfont).grid(row=7,column=1,padx=10)
        Entry(self,textvariable=cvv, width=10).grid(row=7,column=3,pady=10,sticky=W)
        cardNumber=StringVar()
        Label(self,text ='Card Number(16 digits no space): ', font=self.controller.Tfont).grid(row=8,column=1,padx=10)
        Entry(self,textvariable=cardNumber, width=40).grid(row=8,column=3,pady=10,sticky=W)
        Button(self,text="Place Order!",font=self.controller.\
            font,command=lambda:self.placeOrder(billaddress.get(),billname.get(),\
                shipaddress.get(),shipname.get(),cvv.get(),expDate.get(),cardNumber.get(),creditCard.get())).grid(row=9,column=1,pady=30)
        # back to home page button
        Button(self,text="Back to Home Page",font=self.controller.font,command=lambda: self.controller.switch_frame('FirstPage')).grid(row=10,column=1,pady=30)

    def placeOrder(self,billadd,billname,shipadd,shipname,cvv,expDate,cardNum,cardType):
        if billadd==''or billname=='' or shipadd=='' or shipname=='' \
            or len(expDate)!=5 or len(cardNum) !=16 or len(cvv)!=3:
            messagebox.showerror("Error","Please enter the correct information!")
        else:
            cur.execute("select nextval('oidcreater')")
            oid = cur.fetchall()[0][0]
            carriers = ['Canada Post','UPS','DHL','FedEx','Purolator','eShipper','CanPar']
            l = len(carriers)
            carrier = carriers[randint(0,l-1)]
            a = randint(0,2)
            if a==0: 
                status = 'Your order is in transit'
            elif a==1:
                status = "Your order is being packaged in our warehouse, will be shipped soon"
            else:
                status = 'Your order has been delivered'
            today = date.today()
            d = today.strftime("%Y/%m/%d")

            cur.execute("select * from payment_card where card_num=%s",(cardNum,))
            if not cur.fetchall():
                cur.execute('insert into payment_card values (%s,%s,%s,%s,%s,%s)',(cardNum,cvv,expDate,billname,billadd,cardType))
            conn.commit()
            cur.execute('insert into book_order values (%s,%s,%s,%s,%s,%s,%s,%s)',(oid,carrier,self.controller.cid,shipname,shipadd,cardNum,status,d))

            # insert into contain table, map the book with order 
            
            for b in self.controller.cart:              
                cur.execute('insert into contain values (%s,%s,%s)',(oid,b[1],b[2]))
                # reduce the storage of the books the customer bought
                cur.execute('select storage from book where bid=%s',(b[1],))
                storage = cur.fetchall()[0][0]
                storage -= b[2]
                cur.execute('update book set storage = %s where bid=%s',(storage,b[1]))
            # empty the shopping cart
            for b in self.controller.cart:
                cur.execute('delete from shopping_cart where bid=%s',(b[1],))
            cur.execute('REFRESH MATERIALIZED VIEW book_in_order;')
            cur.execute('REFRESH MATERIALIZED VIEW sales_per_author;')
            conn.commit()
            self.controller.cart = []
            messagebox.showinfo("Success","Order Placed Successfully!")
            # Show order number
            messagebox.showinfo("Order Number","Order Number: "+str(oid))
            self.controller.switch_frame('FirstPage')

# order detal pages show details of each order
class OrderPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
    
    def goToHome(self):
        self.booklist.delete(0,END)
        self.status.destroy()
        self.carrier.destroy()
        self.controller.switch_frame('FirstPage')

    def refresh(self):
        # view order
        Label(self,text="View your order: "+str(self.controller.oid),font=("Helvetica", 20)).grid(row=0,column=0,padx=20,pady=20,sticky=W)
        Label(self,text = 'books you ordered:',font=self.controller.Tfont).grid(row=1,column=0,pady=10,padx=20,sticky=W)
        frame = Frame(self)
        frame.grid(column=0,row=2,pady=10,rowspan=4,columnspan=4,sticky=W,padx=20)
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT,fill=Y)
        scrollbarx = Scrollbar(frame,orient='horizontal')
        scrollbarx.pack(side=BOTTOM,fill=X)
        #search result 
        self.booklist = Listbox(frame,height=15,width=100,yscrollcommand=scrollbar.set,xscrollcommand=scrollbarx.set)
        self.booklist.pack(side=LEFT,fill=Y)
        scrollbar.configure(command=self.booklist.yview)
        scrollbarx.configure(command=self.booklist.xview)
        cur.execute("select title,carrier,status,amount from book_in_order where oid=%s",(self.controller.oid,))
        books = cur.fetchall()
        for b in books:
            self.booklist.insert(END,b[0].ljust(100)+"   Amount: "+str(b[3]))
        self.carrier = Label(self,text="Carrier: "+ books[0][1],font=self.controller.Tfont)
        self.carrier.grid(column=0,row=7,pady=10,sticky=W,padx=20)
        self.status = Label(self,text="Shipment Status: "+ books[0][2],font=self.controller.Tfont)
        self.status.grid(column=0,row=8,pady=10,sticky=W,padx=20)
        Button(self,text="Back to Home Page",font=self.controller.font,command=lambda:self.goToHome()).grid(column=0,row=9,pady=10,sticky=W,padx=20)

# show the order numbers the customer has placed 
class GetOrderNumberPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller

    def refresh(self):
        cur.execute("select oid from book_order where cid =%s",(self.controller.cid,))                                                                                                                                           
        orders = cur.fetchall()
        Label(self,text="Your orders number are listed below:",font=self.controller.font).grid(column=0,row=0,pady=20,padx=40,sticky=W)       
        frame = Frame(self)
        frame.grid(column=0,row=1,pady=10,rowspan=2,columnspan=2,padx=40,sticky=W)
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT,fill=Y)
        #search result 
        self.oidlist = Listbox(frame,height=10,width=80,yscrollcommand=scrollbar.set)
        self.oidlist.pack(side=LEFT,fill=Y)
        scrollbar.configure(command=self.oidlist.yview)
        for o in orders:
            self.oidlist.insert(END,o[0])
        Button(self,text="Back to Home Page",font=self.controller.Tfont,command=lambda:self.backToHome()).grid(column=0,row=4,padx=40,sticky=W)
    def backToHome(self):
        self.oidlist.delete(0,END)
        self.controller.switch_frame('FirstPage')


##########################################################################################################
#   Pages for administration:                                                                            #
##########################################################################################################   
# first pages for administration including adding books, publishers, delete boooks
class adminFirstPage(Frame):
    def addPublisher(self,name,add,email,phone,bank):
        cur.execute('select * from publisher where name ILIKE  %s',(name,))
        if cur.fetchall():
            messagebox.showerror("Error","Publisher is already added!")
        else:
            cur.execute("select nextval('pidcreater')")
            pid = cur.fetchall()[0][0]
            cur.execute('INSERT INTO PUBLISHER VALUES (%s,%s,%s,%s,%s,%s)',(name,add,email,phone,bank,pid))
            conn.commit()
            messagebox.showinfo("Success","Publisher saved")
        self.pubname.delete(0,END)
        self.pubadd.delete(0,END)
        self.pubbank.delete(0,END)
        self.pubphone.delete(0,END)
        self.pubemail.delete(0,END)
    def addAuthor(self):
        # case insensitive
        cur.execute('select * from author where name ILIKE %s',(self.author_.get(),))
        if cur.fetchall():
            messagebox.showerror("Error","Author is already added!")
        else:
            cur.execute("select nextval('aidcreater')")
            aid = cur.fetchall()[0][0]
            cur.execute('INSERT INTO author VALUES (%s,%s)',(aid,self.author_.get()))
            conn.commit()
            messagebox.showinfo("Success","Author saved")
        self.author_entry.delete(0,END)
    def addGenre(self):
        # case insensitive
        cur.execute('select * from genre where genre_type ILIKE  %s',(self.genre_.get(),))
        if cur.fetchall():
            messagebox.showerror("Error","Genre is already added!")
        else:
            cur.execute("select nextval('gidcreater')")
            gid = cur.fetchall()[0][0]
            cur.execute('INSERT INTO genre VALUES (%s,%s)',(self.genre_.get(),gid))
            conn.commit()
            messagebox.showinfo("Success","Genre saved")
        self.genre_entry.delete(0,END)

    def addUcost(self):
        month = self.month.get()
        cost = self.ucost.get()
        try:
            cost=float(cost)
        except ValueError:
            messagebox.showerror("Error","Please insert a number for cost")
            self.ucost_entry.delete(0,END)
            return 
       
        self.monthMap={}
        monthList=['January','February','March','April', 'May', 'June', 'July', 'August' ,'September', 'October', 'November', 'December']
        i=1
        for m in monthList:
            if i<10:
                self.monthMap[m] = '0'+str(i)
            else:
                self.monthMap[m] = str(i)
            i+=1
        cur.execute("select cost from utility where month=%s",(self.monthMap[month],))
        if cur.fetchall():
            result = messagebox.askquestion("Update", "Exist Utility record for this month, Click YES to update", icon='warning')
            if result == 'yes':
                cur.execute("update utility set cost=%s where month=%s",(cost,self.monthMap[month]))
                messagebox.showinfo("success","Utility cost updated")
        else:
            cur.execute("update utility set cost=%s where month=%s",(cost,self.monthMap[month]))
            messagebox.showinfo("success","Utility cost updated")
        self.ucost_entry.delete(0,END)
        conn.commit()


    def goToReport(self):
        # refresh the materialized view first
        refreshMaterializeView()
        self.controller.switch_frame('reportFirstPage')


    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller

        
        Label(self,text="Admin Page",font=("Helvetica","20")).grid(column=0,row=0,padx=20,sticky=W,pady=20)
        Button(self,text="View Sales Report",font=controller.font,command=lambda:self.goToReport() ).grid(column=0,row=1,padx=20,sticky=W,pady=10)
        Button(self,text="Back to Home Page",font=controller.font,command=lambda:controller.switch_frame('FirstPage')).grid(column=1,row=1,padx=40,sticky=W,pady=10)
        Button(self,text="Go to Next Page",font=controller.font,command=lambda:controller.switch_frame('adminSecondPage')).grid(column=2,row=1,padx=20,sticky=W,pady=10)
        # this button will go to page that shows all the past orders placed from publisher when book storage < 10
        Button(self,text="Book orders placed",font=controller.font,command=lambda:controller.switch_frame('OrderfromPubPage')).grid(column=3,row=1,padx=20,sticky=W,pady=10)
        # add new publisher
        Label(self,text="Add new publisher:",font=("Helvetica","14","bold")).grid(column=0,row=2,padx=20,sticky=W,pady=10)
        pub_name=StringVar()
        pub_add=StringVar()
        pub_email=StringVar()
        pub_phone=StringVar()
        pub_bank=StringVar()
        Label(self,text="Publisher Name:",font=("Helvetica","14")).grid(column=0,row=3,sticky=W,pady=5,padx=20)  
        self.pubname=Entry(self,textvariable=pub_name,width=30)
        self.pubname.grid(column=1,row=3,sticky=W,pady=5)  
        Label(self,text="Publisher email:",font=("Helvetica","14")).grid(column=0,row=4,sticky=W,pady=5,padx=20)  
        self.pubemail=Entry(self,textvariable=pub_email,width=30)
        self.pubemail.grid(column=1,row=4,sticky=W,pady=5)  
        Label(self,text="Publisher phone:",font=("Helvetica","14")).grid(column=0,row=5,sticky=W,pady=5,padx=20)
        self.pubphone=Entry(self,textvariable=pub_phone,width=30)   
        self.pubphone.grid(column=1,row=5,sticky=W,pady=5)  
        Label(self,text="Publisher address:",font=("Helvetica","14")).grid(column=0,row=6,sticky=W,pady=5,padx=20)
        self.pubadd=Entry(self,textvariable=pub_add,width=50)
        self.pubadd.grid(column=1,row=6,sticky=W,pady=5)
        Label(self,text="Publisher's bank account :",font=("Helvetica","14")).grid(column=0,row=7,sticky=W,pady=5,padx=20)
        self.pubbank=Entry(self,textvariable=pub_bank,width=50)
        self.pubbank.grid(column=1,row=7,sticky=W,pady=5)
        Button(self,text="Save new publisher",font=controller.font,command=lambda:self.addPublisher(pub_name.get(),\
            pub_add.get(),pub_email.get(),pub_phone.get(),pub_bank.get())).grid(column=0,row=8,sticky=W,pady=5,padx=20)

        # add new author:
        self.author_=StringVar()
        Label(self,text="Add new author:",font=("Helvetica","14","bold")).grid(column=0,row=9,padx=20,sticky=W,pady=5)
        self.author_entry=Entry(self,textvariable=self.author_,width=30)
        self.author_entry.grid(column=1,row=9,sticky=W,pady=5)
        Button(self,text="save",font=controller.font,command=lambda:self.addAuthor()).grid(column=2,row=9,sticky=W,pady=5)
        # add new genre:
        self.genre_=StringVar()
        Label(self,text="Add new genre:",font=("Helvetica","14","bold")).grid(column=0,row=10,padx=20,sticky=W,pady=5)
        self.genre_entry=Entry(self,textvariable=self.genre_,width=30)
        self.genre_entry.grid(column=1,row=10,sticky=W,pady=5)
        Button(self,text="save",font=controller.font,command=lambda: self.addGenre()).grid(column=2,row=10,sticky=W,pady=5)
        # add utility cost
        Label(self,text="Add Utility Cost:",font=("Helvetica","14","bold")).grid(column=0,row=11,padx=20,sticky=W,pady=5)
        OPTIONS = ['January','February','March','April', 'May', 'June','July', 'August' ,'September', 'October', 'November', 'December']
        self.month = StringVar()
        self.month.set(OPTIONS[0])
        Label(self,text="Select Month:",font=("Helvetica","14")).grid(column=0,row=12,padx=20,sticky=W,pady=5)
        OptionMenu(self, self.month, *OPTIONS).grid(row=12,column=1,pady=10,sticky=W)
        Label(self,text="Cost($):",font=("Helvetica","14")).grid(column=2,row=12,sticky=W,pady=5)
        self.ucost = StringVar()
        self.ucost_entry=Entry(self,textvariable=self.ucost,width=30)
        self.ucost_entry.grid(column=3,row=12,sticky=W,pady=5)
        Button(self,text="save",font=controller.font,command=lambda:self.addUcost()).grid(column=0,row=13,sticky=W,pady=5,padx=20)

# second pages for administration including adding books, publishers, delete boooks
class adminSecondPage(Frame):
    def addBook(self):
        cur.execute('select * from book where title ILIKE %s',(self.book_title.get(),))
        if cur.fetchall():
            messagebox.showerror("Error","Book with this title has been added")
        elif self.book_title.get()=='' or len(self.book_ISBN.get()) !=13:

            messagebox.showerror("Error","Please enter title or correct ISBN")
        else:
            cur.execute('select * from book where ISBN = %s',(self.book_ISBN.get(),))
            if cur.fetchall():
                messagebox.showerror("Error","Book with this ISBN has been added")
            else:
                try:
                    price = float(self.book_price.get())
                    pages = int(self.book_page.get())
                    storage = int(self.book_storage.get())
                except ValueError:
                    messagebox.showerror("Error","Please enter numeric numbers for price, page count or storage")
                aid_list=set()
                cur.execute('select pid from publisher where name ILIKE %s',(self.book_publisher.get(),))
                pid = cur.fetchall()
                if pid:
                    pid=pid[0][0]
                    # assign a new id to this book
                    cur.execute("select nextval('bidcreater')")
                    bid = cur.fetchall()[0][0]
                    authors = self.book_author.get().split(",")
                    aid_list=[]
                    for a in authors:
                        a=a.strip()
                        cur.execute('select aid from author where name ILIKE %s', (a,))
                        aid = cur.fetchall()
                        if aid:
                            aid = aid[0][0]
                        else:
                            # if this author is a new author, add he/she directly to database
                            cur.execute("select nextval('aidcreater')")
                            aid = cur.fetchall()[0][0]
                            cur.execute('INSERT INTO author VALUES (%s,%s)',(aid,a))
                            messagebox.showinfo("success","new author has been added")
                            conn.commit()                       
                        aid_list.append(aid)
                    
                    # genre

                    genres = self.book_genre.get().split(",")
                    gid_list=[]
                    for g in genres:
                        g=g.strip()

                        cur.execute('select gid from genre where genre_type ILIKE %s', (g,))
                        gid = cur.fetchall()

                        if gid:
                            gid=gid[0][0]
                        else:
                            # if this author is a new author, add he/she directly to database
                            cur.execute("select nextval('gidcreater')")
                            gid = cur.fetchall()[0][0]
                            cur.execute('INSERT INTO genre VALUES (%s,%s)',(g,gid))
                            messagebox.showinfo("success","new genre has been added")
                            conn.commit()
                        gid_list.append(gid)
                    percent = float(self.addpercent.get())
                    #add other infomations for this book
                    cur.execute('INSERT INTO BOOK VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(self.book_title.get(),price,pages,self.book_ISBN.get(),storage,bid,pid,percent))
                    conn.commit()
                    # map authors to this book
                    for a in aid_list:
                        cur.execute('INSERT INTO write VALUES (%s,%s)',(a,bid))
                    # map genres to this book
                    for g in gid_list:
                        cur.execute('INSERT INTO TYPEOF VALUES (%s,%s)',(g,bid))
                        conn.commit()
                        refreshMaterializeView()
                    messagebox.showinfo("Success","This book has been adde to database")
                    self.addtitle.delete(0,END)
                    self.addISBN.delete(0,END)
                    self.addprice.delete(0,END)
                    self.addstorage.delete(0,END)
                    self.addpage.delete(0,END)
                    self.publisher_entry.delete(0,END)
                    self.author_entry.delete(0,END)
                    self.genre_entry.delete(0,END)  
                else:
                    messagebox.showwarning("Warning","Please add this publisher first!")
  

    def serachDelteBook(self,title,ISBN):   
        # clean the list box first   
        self.delResult.delete(0,END)

        if ISBN != "":
            cur.execute('select * from book where ISBN = %s',(ISBN,))
            for book in cur.fetchall():
                self.delResult.insert(END,book[0])
            return
        cur.execute('select DISTINCT ct.title from ct where ct.title ILIKE %s',('%'+title+'%',))
        for book in cur.fetchall():
                self.delResult.insert(END,book[0])
        return
        
    def deleteSelected(self):
        values = self.delResult.curselection()
        if values:
            title = self.delResult.get(values[0])
            messagebox.askquestion("question","Are you sure to delete this book?")
            cur.execute('delete from book where title=%s',(title,))
            conn.commit()
            refreshMaterializeView()
            messagebox.showinfo("success","book has been deleted")
        else:
            messagebox.showwarning("Error", "Warning:Please select a book to delete")


    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        Label(self,text="Admin Page",font=("Helvetica","20")).grid(column=0,row=0,padx=20,sticky=W,pady=20)
        Button(self,text="Back to Home Page",font=controller.font,command=lambda:controller.switch_frame('FirstPage')).grid(column=0,row=1,padx=20,sticky=W,pady=10)
        Button(self,text="Back to Previous Page",font=controller.font,command=lambda:controller.switch_frame('adminFirstPage')).grid(column=1,row=1,padx=20,sticky=W,pady=10)
        #add new book
        Label(self,text="Add new book:",font=("Helvetica","14","bold")).grid(column=0,row=2,padx=20,sticky=W,pady=10)
        self.book_title=StringVar()
        self.book_author=StringVar()
        self.book_ISBN=StringVar()
        self.book_publisher=StringVar()
        self.book_price=StringVar()
        self.book_page=StringVar()
        self.book_storage=StringVar()
        self.book_genre=StringVar()
        self.book_percent=StringVar()
        Label(self,text="Book Title:",font=("Helvetica","14")).grid(column=0,row=3,padx=20,sticky=W,pady=5)
        self.addtitle=Entry(self,textvariable=self.book_title,width=30)
        self.addtitle.grid(column=1,row=3,sticky=W,pady=5)
        Label(self,text="Book ISBN(13 digits):",font=("Helvetica","14")).grid(column=2,row=3,sticky=W,pady=5,padx=20)
        self.addISBN=Entry(self,textvariable=self.book_ISBN,width=30)
        self.addISBN.grid(column=3,row=3,sticky=W,pady=5)
        Label(self,text="Book price($):",font=("Helvetica","14")).grid(column=0,row=4,padx=20,sticky=W,pady=5)
        self.addprice=Entry(self,textvariable=self.book_price,width=30)
        self.addprice.grid(column=1,row=4,sticky=W,pady=5)
        Label(self,text="Page Count :",font=("Helvetica","14")).grid(column=2,row=4,sticky=W,pady=5,padx=20)
        self.addpage=Entry(self,textvariable=self.book_page,width=30)
        self.addpage.grid(column=3,row=4,sticky=W,pady=5)
        Label(self,text="Storage :",font=("Helvetica","14")).grid(column=0,row=5,sticky=W,pady=5,padx=20)
        self.addstorage=Entry(self,textvariable=self.book_storage,width=30)
        self.addstorage.grid(column=1,row=5,sticky=W,pady=5)
        Label(self,text="percentage to publisher(in form of 0.xx) :",font=("Helvetica","14"),wraplength=250).grid(column=2,row=5,sticky=W,pady=5,padx=20)
        self.addpercent=Entry(self,textvariable=self.book_percent,width=30)
        self.addpercent.grid(column=3,row=5,sticky=W,pady=5)

        Label(self,text="Publisher:",font=("Helvetica","14")).grid(column=0,row=6,sticky=W,pady=5,padx=20)
        self.publisher_entry=Entry(self,textvariable=self.book_publisher,width=50)
        self.publisher_entry.grid(column=1,row=6,sticky=W,pady=5)    
        Label(self,text="Author(seperate by ','):",font=("Helvetica","14")).grid(column=0,row=7,sticky=W,pady=5,padx=20)
        self.author_entry = Entry(self,textvariable=self.book_author,width=50)   
        self.author_entry.grid(column=1,row=7,sticky=W,pady=5)     
        Label(self,text="Genre(seperate by ','):",font=("Helvetica","14")).grid(column=0,row=8,sticky=W,pady=5,padx=20)
        self.genre_entry =  Entry(self,textvariable=self.book_genre,width=50)
        self.genre_entry.grid(column=1,row=8,sticky=W,pady=5)
        Button(self,text="Save new Book",font=controller.font,command=lambda:self.addBook()).grid(column=2,row=8,sticky=W,pady=5,padx=20)

        # delete book
        self.delete_title=StringVar()
        self.delete_ISBN=StringVar()
        Label(self,text="Delete book:",font=("Helvetica","14","bold")).grid(column=0,row=10,padx=20,sticky=W,pady=10)
        Label(self,text="search by title:",font=controller.Tfont).grid(column=0,row=11,padx=20,sticky=W,pady=10)
        Entry(self,textvariable=self.delete_title,width=30).grid(column=1,row=11,sticky=W,pady=10)
        Label(self,text="search by ISBN:",font=controller.Tfont).grid(column=2,row=11,padx=20,sticky=W,pady=10)
        Entry(self,textvariable=self.delete_ISBN,width=30).grid(column=3,row=11,sticky=W,pady=10)
        Button(self,font=controller.font,text='search')
        self.delResult = Listbox(self,height=3,width=50)
        self.delResult.grid(column=1,row=12,sticky=W,pady=10)
        Button(self,text='search',font=controller.font,command=lambda:self.serachDelteBook(self.delete_title.get(),self.delete_ISBN.get())).grid(column=2,row=12,padx=20,sticky=W,pady=10)
        Button(self,font=controller.font,text='Delete this book',command=lambda:self.deleteSelected()).grid(column=1,row=13,sticky=W,pady=10)
    
# page shows the order history that the bookstore ordered from the publisher
# in the real word, this page will be replaced by an email sending component
# the email request will be sent according to the information shown in this page
class OrderfromPubPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        
    def refresh(self):
        cur.execute('REFRESH MATERIALIZED VIEW book_order_record;')
        conn.commit()
        Label(self,text="Past Order Placed to Publishers",font=("Helvetica",'20')).grid(column=0,row=0,padx=20,pady=20,sticky=W)
        self.frame= Frame(self)
        self.frame.grid(column=0,row=1,padx=20,pady=10)
        scrollbar1 = Scrollbar(self.frame)
        scrollbar1.pack(side=RIGHT,fill=Y)
        scrollbar2 = Scrollbar(self.frame,orient='horizontal')
        scrollbar2.pack(side=BOTTOM,fill=X)
        self.record = Listbox(self.frame,font="Consolas",height=25,width=120,yscrollcommand=scrollbar1.set,xscrollcommand=scrollbar2.set)
        self.record.pack(side=LEFT,fill=Y)
        scrollbar1.configure(command=self.record.yview)
        scrollbar2.configure(command=self.record.xview)

        cur.execute("select * from book_order_record order by date asc;")
        records = cur.fetchall()
        self.record.insert(END,"Publisher".ljust(50)+"email".ljust(40)+"Book Title".ljust(200)+"ISBN".ljust(20)+"Amount Ordered".ljust(20)+"Date Ordered".ljust(20))
        for a in records:           
            self.record.insert(END,f"{a[0].ljust(50)}{a[1].ljust(40)}{a[2].ljust(200)}{a[3].ljust(20)}{str(a[4]).ljust(20)}{str(a[5]).ljust(20)}")
        Button(self,text="Back to Admin Page",font=self.controller.font,command=lambda: self.controller.switch_frame('adminFirstPage') ).grid(column=0,row=6,padx=20,pady=20,sticky=W)

# the first page for the admin to view the sales reports, letting the admin choose the month of report they want to view
class reportFirstPage(Frame):  
    def goToReport(self,month):
        self.controller.month=month
        self.controller.switch_frame('reportSecondPage')
        
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller  
        Label(self,text="Report Page One",font=("Helvetica",'20')).grid(column=0,row=0,padx=20,pady=20,sticky=W)
        Label(self,text="Select the month you want to view:",font=controller.Tfont).grid(column=0,row=1,padx=20,pady=20,sticky=W)
        Button(self,text="Back to Admin Page",font=controller.font,width=17,command=lambda:controller.switch_frame('adminFirstPage')).grid(column=1,row=0)
        Button(self,text="Back to Home Page",font=controller.font,width=17,command=lambda:controller.switch_frame('FirstPage')).grid(column=2,row=0)
        monthL=['January','February','March','April', 'May', 'June']
        monthR=[ 'July', 'August' ,'September', 'October', 'November', 'December']
        r=2
        for m in monthL:
            Button(self,text=m,font=controller.font,command=lambda j=m: self.goToReport(j),width=10).grid(column=1,row=r,pady=10,padx=40)
            r+=1
        r=2
        for m in monthR:
            Button(self,text=m,font=controller.font,command=lambda j=m: self.goToReport(j),width=10).grid(column=2,row=r,pady=10,padx=70)
            r+=1

# the second page for the admin to view the sales reports, letting the the admin choose the type of report they want to view
class reportSecondPage(Frame):  
    def goToReport(self,report):
        self.controller.report=report
        self.controller.switch_frame('reportThirdPage')
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller  
        Label(self,text="Report Page Two",font=("Helvetica",'20')).grid(column=0,row=0,padx=20,pady=20,sticky=W)
        Label(self,text="Select the report you want to view:",font=controller.Tfont).grid(column=0,row=1,padx=20,pady=20,sticky=W)
        Button(self,text="Back to Admin Page",font=controller.font,width=17,command=lambda:controller.switch_frame('adminFirstPage')).grid(column=1,row=0,padx=10)
        Button(self,text="Back to Home Page",font=controller.font,width=17,command=lambda:controller.switch_frame('FirstPage')).grid(column=2,row=0)
        reports=['Sales vs Author','Sales vs Genres','Sales vs Expenditure', 'Money sent to Publisher']
        rr=2
        for r in reports:
            Button(self,text=r,font=controller.font,command=lambda j=r: self.goToReport(j),width=20).grid(column=1,row=rr,pady=10,padx=40)
            rr+=1
        Button(self,text="Change Month",font=controller.font,width=17,command=lambda:controller.switch_frame('reportFirstPage')).grid(column=1,row=7,pady=40)

# the second page for the admin to view the sales reports, showing the details of the reports
class reportThirdPage(Frame):       
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller  
        self.monthMap={}
        monthList=['January','February','March','April', 'May', 'June', 'July', 'August' ,'September', 'October', 'November', 'December']
        i=1
        for m in monthList:
            if i<10:
                self.monthMap[m] = '0'+str(i)
            else:
                self.monthMap[m] = str(i)
            i+=1

    def refresh(self):
        month = self.controller.month
        report = self.controller.report

        for widget in self.winfo_children():
           widget.destroy() 
        # create structure
        Label(self,text=report +" Report of "+month,font=("Helvetica",'20')).grid(column=0,row=0,padx=20,pady=20,sticky=W)
        self.frame= Frame(self)
        self.frame.grid(column=0,row=1,padx=20,pady=10)
        scrollbar1 = Scrollbar(self.frame)
        scrollbar1.pack(side=RIGHT,fill=Y)
        self.record = Listbox(self.frame,font="Consolas",height=25,width=120,yscrollcommand=scrollbar1.set)
        self.record.pack(side=LEFT,fill=Y)
        scrollbar1.configure(command=self.record.yview)


        if report == 'Sales vs Author':
            cur.execute("select name,price from sales_per_author where month=%s order by price desc",(self.monthMap[month],))
            arecords = cur.fetchall()
            for a in arecords:
                self.record.insert(END, f"Author Name: {a[0].ljust(50)} Sales: {str(a[1])}")
        elif report == "Sales vs Genres":
            cur.execute("select type,price from sales_per_genre where month=%s order by price desc",(self.monthMap[month],))
            grecords = cur.fetchall()
            for g in grecords:
                self.record.insert(END, f"Genre Type: {g[0].ljust(50)} Sales: {str(g[1])}")
        elif report == 'Sales vs Expenditure':
            scrollbar1.destroy()
            self.record.destroy()
            self.frame.grid_forget()
            self.frame.destroy()
            cur.execute("select month,sales,expen, profit,utility,pay_pub from sales_vs_expenditure where month=%s",(self.monthMap[month],))
            erecords = cur.fetchall()
            e=erecords[0]
            self.l1 =Label(self,text =  f"Sales: ${str(e[1]).ljust(20)}", font = ("Helvetica",'18'))
            self.l1.grid(column=0,row=1,padx=20,pady=10,sticky=W)
            self.l2 =Label(self,text =  f"Expenditure: ${str(round(e[2],2)).ljust(20)}", font = ("Helvetica",'18'))
            self.l2.grid(column=0,row=2,padx=20,pady=10,sticky=W)
            self.l3 =Label(self,text =  f"Profit: ${str(round(e[3],2)).ljust(20)}", font = ("Helvetica",'18'))
            self.l3.grid(column=0,row=3,padx=20,pady=10,sticky=W)    
            self.l4 =Label(self,text =  f"Utility: ${str(round(e[4],2)).ljust(20)}", font = ("Helvetica",'18'))
            self.l4.grid(column=0,row=4,padx=20,pady=10,sticky=W)
            self.l5 =Label(self,text =  f"Money Paid to Publisher: ${str(round(e[5],2)).ljust(20)}", font = ("Helvetica",'18'))
            self.l5.grid(column=0,row=5,padx=20,pady=10,sticky=W) 
        else:
            cur.execute('''select pname,sale, publisher.BANK_ACC  
            from sales_to_publisher, publisher
            where month=%s and sales_to_publisher.pname = publisher.name order by sale desc''',(self.monthMap[month],))
            precords = cur.fetchall()
            for p in precords:
                self.record.insert(END, f"Name: {p[0].ljust(50)} Sales: {str(round(p[1],1)).ljust(15)} Bank Account: {p[2]}")

        Button(self,text="Back to Previous Page",font=self.controller.font,width=20,command=lambda:self.controller.switch_frame('reportSecondPage')).grid(column=0,row=7,padx=10,pady=20)

# disconnect the database and then close the app window
def on_closing():
    cur.close()
    conn.close()
    app.destroy()
    print("database disconnected")

if __name__ == '__main__':
    #connect to database
    conn = psycopg2.connect(
    dbname = database,
    user = username,
    password = pwd,
    host = hostname)
    cur=conn.cursor() 
    print("database connected")
    
    # run GUI
    app = BookStoreAppGUI()
    app.geometry('1150x700')
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
    