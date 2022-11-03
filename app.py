from tkinter import *
import tkinter.font as TkFont


class BookStoreAppGUI(Tk):
    # initialize the GUI class
    def __init__(self):
        # initialize the Tk
        Tk.__init__(self)
        # set font here
        self.font = TkFont.Font(family="Helvetica", size="16",weight='bold')
        self.Tfont = TkFont.Font(family="Helvetica", size="14")
        

        # The big container containers all the frames
        container = Frame()
        container.grid(row=0,column=0)

        # the list containing all the frames
        self.frame_list={}

        # create all the frames from each page class
        # ,CartPage,BookPage,CheckoutPage,\
        #     OrderPage,TrackPage,AdminPage,ReportPage,AdminLoginPage
        for p in (FirstPage,AdminLoginPage,UserLoginPage):
            name = p.__name__
            frame = p(parent=container,controller=self)
            frame.grid(row=0,column=0,sticky="nsew")
            self.frame_list[name] = frame
        
        self.switch_frame('FirstPage')

    # switch between frames
    def switch_frame(self,name):
        page = self.frame_list[name]
        page.tkraise()

class AdminLoginPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        # back to home page
        Home_btn=Button(self,text ='Back to Home', font=controller.font,command=lambda: controller.switch_frame('FirstPage'))\
        .place(relx=.8, rely=.2,anchor= CENTER)

        # Admin name
        text=StringVar()
        name_label=Label(self,text ='Admin Name: ', font=controller.font,pady=50).place(relx=.38, rely=.5,anchor= CENTER)
        name_entry=Entry(self,textvariable=text, width=30).place(relx=.6, rely=.5,anchor= CENTER)
        # Admin Password
        psw_label=Label(self,text ='Admin Password: ',font=controller.font).place(relx=.35, rely=.6,anchor= CENTER)
        psw_entry=Entry(self,textvariable=text,width=30).place(relx=.6, rely=.6,anchor= CENTER)
        # Login button
        Login_btn=Button(self,text ='Log in', font=controller.font).place(relx=.52, rely=.8,anchor= CENTER)

class UserLoginPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        # back to home page
        Home_btn=Button(self,text ='Back to Home', font=controller.font,command=lambda: controller.switch_frame('FirstPage'))\
        .place(relx=.8, rely=.2,anchor= CENTER)

        # Admin name
        text=StringVar()
        name_label=Label(self,text ='User Name: ', font=controller.font,pady=50).place(relx=.38, rely=.5,anchor= CENTER)
        name_entry=Entry(self,textvariable=text, width=30).place(relx=.6, rely=.5,anchor= CENTER)
        # Admin Password
        psw_label=Label(self,text ='User Password: ',font=controller.font).place(relx=.35, rely=.6,anchor= CENTER)
        psw_entry=Entry(self,textvariable=text,width=30).place(relx=.6, rely=.6,anchor= CENTER)
        # Login button
        Login_btn=Button(self,text ='Log in', font=controller.font).place(relx=.52, rely=.8,anchor= CENTER)

   

class FirstPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        # controller help children page get properties from the big frame
        self.controller=controller
        self.content(controller)
        

    def content(self,controller):
        #nevigator
        Adminlogin_btn=Button(self,text ='Admin Login', font=controller.font,command=lambda: controller.switch_frame('AdminLoginPage'))
        Adminlogin_btn.grid(row=0,column=1,pady=20)
        Userlogin_btn=Button(self,text ='User Login', font=controller.font,command=lambda: controller.switch_frame('UserLoginPage'))
        Userlogin_btn.grid(row=0,column=2)
        Cart_btn=Button(self,text ='Shopping Cart', font=controller.font)
        Cart_btn.grid(row=0,column=3)

        slogan_label=Label(self,text ='Search your book!', font=TkFont.Font(family="Helvetica", size="25",weight='bold'),pady=30)
        slogan_label.grid(row=1,column=1)
        # book information
        text=StringVar()
        book_label=Label(self,text ='Book Name: ', font=controller.Tfont,pady=20)
        book_label.grid(row=2,column=0)
        book_entry=Entry(self,textvariable=text, width=40)
        book_entry.grid(sticky=W,row=2,column=1)
        # author information
        author_label=Label(self,text ='Author Name: ',font=controller.Tfont)
        author_label.grid(row=2,column=2)
        author_entry=Entry(self,textvariable=text,width=40)
        author_entry.grid(sticky=W,row=2,column=3)
        # ISBN information
        ISBN_label=Label(self,text ='ISBN: ', font=controller.Tfont)
        ISBN_label.grid(row=3,column=0)
        ISBN_entry=Entry(self,textvariable=text,width=40)
        ISBN_entry.grid(sticky=W,row=3,column=1)
        # genre information
        genre_label=Label(self,text ='Genre: ', font=controller.Tfont)
        genre_label.grid(row=3,column=2)
        genre_entry=Entry(self,textvariable=text, width=40)
        genre_entry.grid(sticky=W,row=3,column=3)

        #search button
        search_btn = Button(self,text ="Search",font=controller.Tfont,width=12)
        search_btn.grid(sticky=W,row=4,column=1,pady=50)


if __name__ == '__main__':
    app = BookStoreAppGUI()
    app.geometry('900x700')
    app.mainloop()




    