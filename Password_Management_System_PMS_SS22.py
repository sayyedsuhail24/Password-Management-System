#Importing the modules needed for our Passowrd Management System(PMS)
from tkinter import *
from tkinter import messagebox
from random import randint,choice
import sqlite3
import string

# This block is used to login into the system
def login():
    user = username.get() #we are getting the input of the user
    swd = pwdd.get()

    #The system will login as per the given credentials as
    if user == "Admin" and swd == "Admin@123":
        Tr = Toplevel(loginscreen)  #https://docs.python.org/3/library/tk.html
        Tr.title("Login")
        Tr.geometry("1280x720")
        Tr.configure(bg="black")
        Tr.resizable(False, False)
        sampass = Tk()
        sampass.title("Password Management System (PMS)")
        sampass.geometry("500x400")
        sampass.minsize(800, 800)
        sampass.maxsize(800, 800)

        frame = Frame(sampass, bg="#ede3d6", bd=5) #Attributes
        frame.place(relx=0.50, rely=0.50, relwidth=0.98, relheight=0.45, anchor="n") #placement of the window for login

        # Creating the Database for Storing the User Information
        conn = sqlite3.connect("passmanager.db") #connecting the database
        cursor = conn.cursor()

        # We are creating the table as per below lines
        cursor.execute(""" CREATE TABLE IF NOT EXISTS manager (
                              app_name text,
                               url text,
                               email_id text,
                               password text
                               )
       """) #creating the table if it does not exist getting the values as storing in the table

        # The below commands are for Commit and close the changes
        conn.commit()
        conn.close()

        # This block is the submit function for database
        def submit():
            # connect to database
            conn = sqlite3.connect("passmanager.db")
            cursor = conn.cursor()
            #a new database will be created as per this
            # We Insert the data into the Table if the data as per the below if loop
            if app_name.get() != "" and url.get() != "" and email_id.get() != "" and password.get() != "":
                cursor.execute("INSERT INTO manager VALUES (:app_name, :url, :email_id, :password)",
                               {
                                   'app_name': app_name.get(),
                                   'url': url.get(),
                                   'email_id': email_id.get(),
                                   'password': password.get()
                               }
                               )
                # Commit changes
                conn.commit()
                # Close connection
                conn.close()
                # Message box
                messagebox.showinfo("Information for you", "Record Added in Database!")

                # After data entry clear the text boxes
                app_name.delete(0, END)
                url.delete(0, END)
                email_id.delete(0, END)
                password.delete(0, END)

            else:
                messagebox.showinfo("Alert", "Please fill all details!")
                conn.close()

        # Create Query Function
        def query():
            # set button text
            query_btn.configure(text="Hide Records", command=hide) #to Hide the records in the same
            # connect to database
            conn = sqlite3.connect("passmanager.db")
            cursor = conn.cursor()

            # Query the database
            cursor.execute("SELECT *, oid FROM manager")
            records = cursor.fetchall()
            # print(records)

            p_records = ""
            for record in records:
                p_records += str(record[4]) + " " + str(record[0]) + " " + str(record[1]) + " " + str(
                    record[2]) + " " + str(
                    record[3]) + "\n"
            query_label['text'] = p_records
            conn.commit()  # commiting and closing
            conn.close()

        # This function is used to delete the existing records which are already stored
        def delete():
            conn = sqlite3.connect("passmanager.db")
            cursor = conn.cursor()

            # Query the database
            t = delete_id.get()
            if (t != ""):
                cursor.execute("DELETE FROM manager where oid = " + delete_id.get())
                delete_id.delete(0, END)
                messagebox.showinfo("Alert", "Record %s Deleted" % t)

            else:
                messagebox.showinfo("Alert", "Please enter record id to delete!")
            conn.commit()
            conn.close()
        #This function is used to update the exisitng records in the system

        def update():
            t = update_id.get()
            if (t != ""):
                global edit
                edit = Tk()
                edit.title("Update Record")
                edit.geometry("500x400")
                edit.minsize(450, 300)
                edit.maxsize(450, 300)
                global app_name_edit, url_edit, email_id_edit, password_edit

                app_name_edit = Entry(edit, width=30)
                app_name_edit.grid(row=0, column=1, padx=20)
                url_edit = Entry(edit, width=30)
                url_edit.grid(row=1, column=1, padx=20)
                email_id_edit = Entry(edit, width=30)
                email_id_edit.grid(row=2, column=1, padx=20)
                password_edit = Entry(edit, width=30)
                password_edit.grid(row=3, column=1, padx=20)

                app_name_label_edit = Label(edit, text="Application Name:")
                app_name_label_edit.grid(row=0, column=0)
                url_label_edit = Label(edit, text="URL:")
                url_label_edit.grid(row=1, column=0)
                email_id_label_edit = Label(edit, text="Email Id:")
                email_id_label_edit.grid(row=2, column=0)
                password_label_edit = Label(edit, text="Password:")
                password_label_edit.grid(row=3, column=0)

                # Create Save Button
                submit_btn_edit = Button(edit, text="Save Record", command=change)
                submit_btn_edit.grid(row=4, column=0, columnspan=2, pady=5, padx=15, ipadx=135)

                # connect to database
                conn = sqlite3.connect("passmanager.db")
                cursor = conn.cursor()

                # Query the database
                cursor.execute("SELECT * FROM manager where oid = " + update_id.get())
                records = cursor.fetchall()

                for record in records:
                    app_name_edit.insert(0, record[0])
                    url_edit.insert(0, record[1])
                    email_id_edit.insert(0, record[2])
                    password_edit.insert(0, record[3])

                    conn.commit()
                    conn.close()

            else:
                messagebox.showinfo("Alert", "Please enter record id to update!")
        #C
        def change():
            # connect to database
            conn = sqlite3.connect("passmanager.db")
            cursor = conn.cursor()

            # Insert Into Table
            if app_name_edit.get() != "" and url_edit.get() != "" and email_id_edit.get() != "" and password_edit.get() != "":
                cursor.execute("""UPDATE manager SET 
                                app_name = :app_name,
                                url = :url,
                                email_id = :email_id,
                                password = :password

                                WHERE oid = :oid""",
                               {
                                   'app_name': app_name_edit.get(),
                                   'url': url_edit.get(),
                                   'email_id': email_id_edit.get(),
                                   'password': password_edit.get(),
                                   'oid': update_id.get()
                               }
                               )

            else:
                messagebox.showinfo("Alert", "Please fill all details!")
                conn.close()
        #This function is used to hide the data from the form recrds
        def hide():
            query_label['text'] = ""
            query_btn.configure(text="Show Records", command=query)
        #pass starting point
        def Password_generator():
            def passwordc():
                pmin = 5 # min lenght of password to be generated
                pmax = 12 #max length of password generated
                all_password = string.ascii_letters + string.punctuation + string.digits #combining all characters, letters and punctuations for our random password generation
                pgen = ''.join(choice(all_password)
                                             for x in range(randint(pmin, pmax))) # we are using for loop to iterate and get random passwords
                display.delete(0, END)
                display.insert(0, pgen)

            bb = Tk() #using Tkinter framework again for password generator
            bb.geometry("400x400")
            bb.title("Password Generator")
            big_title = Label(bb, text='Password Generator', font=('times', 30), bg='#b5007c', fg='white') #attributes
            big_title.pack()
            width = 250
            height = 250
            display = Entry(bb, font=('times', 30), bg='white', fg='black')
            display.pack()
            button = Button(bb, font=('times', 25), border=0, text='Generator', bg='red', fg='white',
                            command=passwordc) #creation of buttons
            button.pack(expand=YES)



            bb.mainloop()

        # Creation of Text Boxes
        app_name = Entry(sampass, width=30)
        app_name.grid(row=0, column=1, padx=20)
        url = Entry(sampass, width=30)
        url.grid(row=1, column=1, padx=20)
        email_id = Entry(sampass, width=30)
        email_id.grid(row=2, column=1, padx=20)
        password = Entry(sampass, width=30)
        password.grid(row=3, column=1, padx=20)
        delete_id = Entry(sampass, width=20)
        delete_id.grid(row=6, column=1, padx=20)
        update_id = Entry(sampass, width=20)
        update_id.grid(row=7, column=1, padx=20)

        # We are creating Text Labels Box
        application_name_label = Label(sampass, text="Name of the Application being used:")
        application_name_label.grid(row=0, column=0)
        Link_label = Label(sampass, text="Link of the Application:")
        Link_label.grid(row=1, column=0)
        credential_id_label = Label(sampass, text="Email Id or User Name:")
        credential_id_label.grid(row=2, column=0)
        passwordcredential_label = Label(sampass, text="Password:")
        passwordcredential_label.grid(row=3, column=0)
        # delete_label = Label(sampass, text = "Delete Record#:")
        # delete_label.grid(row=6, column=1)

        # Create Submit Button
        submit_btn = Button(sampass, text="Add Record", command=submit)
        submit_btn.grid(row=5, column=0, pady=5, padx=15, ipadx=35)

        # Query Button Creation
        query_btn = Button(sampass, text="Show Records", command=query)
        query_btn.grid(row=5, column=1, pady=5, padx=5, ipadx=35)

        # Delete Button Creation
        delete_btn = Button(sampass, text="Delete Record", bg='#ffb3fe', command=delete)
        delete_btn.grid(row=6, column=0, ipadx=30)

        # Update Button Creation
        update_btn = Button(sampass, text="Update Record", bg='blue', command=update)
        update_btn.grid(row=7, column=0, ipadx=30)

        # Password Random Generator Function
        pass_gen = Button(sampass, text="Password Generator", command=Password_generator)
        pass_gen.grid(row=8, column=0, ipadx=30)

        # Create a Label to show responses
        global query_label
        query_label = Label(frame, anchor="nw", justify="left")
        query_label.place(relwidth=1, relheight=1)




    #using else if condition to deny access as the other possibilities are there for login
    elif user == "" and pwdd == "":
        messagebox.showerror("Access Denied", "The password is incorrect please check the credentials")

    elif user == "":
        messagebox.showerror("Access Denied", "Please enter the correct credentials")

    elif pwdd == "":
        messagebox.showerror("Access Denied", "Please enter the correct credentials")

    elif user != "Admin" and pwdd == "Shoaib@123":
        messagebox.showerror(("Access Denied", "Please enter the correct credentials"))

#Main login screen block
def mainloginscree():
    global loginscreen #Declaring global for the variables
    global username
    global pwdd
    loginscreen = Tk()
    labletitle = Label(text="Password Management System ")
    loginscreen.geometry("1280x720") #size of the framework of login

    labletitle.pack(pady=50)
    Bcolor = Frame(loginscreen, bg="red", width=800, height=400)
    Bcolor.pack

    mframe = Frame(loginscreen, bg="black", width=800, height="400")
    mframe.pack(padx=20, pady=20)

    Label(mframe, text="Username or mailid", font=("Times", 15, "bold")).place(x=150, y=30) #Attributes
    Label(mframe, text="password of the user", font=("Times", 15, "bold")).place(x=150, y=50) #Attributes

    username = StringVar()
    pwdd = StringVar()
    toenterusername = Entry(mframe, textvariable=username, width=10, font=("arial", 15))
    toenterusername.place(x=400, y=30)
    toenterpassword = Entry(mframe, textvariable=pwdd, width=10, show="*")
    toenterpassword.place(x=400, y=50)

    #Reset block essentially to reset data
    def reset():
        toenterusername.delete(0, END)
        toenterpassword.delete(0, END)

    #Register for a new user function
    def register():
        fv = Tk()
        fv.geometry("500x500")
        fv.title("Register form")
        #This block is used for creating a table and storing data pertaining to register form
        def Database():
            global conn, cursor
            conn = sqlite3.connect("db_member.db")
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT)")

        def registerf():
            mailiduser = StringVar()
            pwd = StringVar()
            Userfirstname = StringVar()
            userlastname = StringVar()

        global RegisterFrame, lbl_result2
        RegisterFrame = Frame(fv)
        RegisterFrame.grid(row=0, padx=30)
        usernamelabel = Label(RegisterFrame, text="Username:", font=('times', 18), bd=18)
        usernamelabel.grid(row=1)
        passwordlabel = Label(RegisterFrame, text="Password:", font=('times', 18), bd=18)
        passwordlabel.grid(row=2)
        firstnamelabel = Label(RegisterFrame, text="Firstname:", font=('times', 18), bd=18)
        firstnamelabel.grid(row=3)
        lastnamelabel = Label(RegisterFrame, text="Lastname:", font=('times', 18), bd=18)
        lastnamelabel.grid(row=4)
        registerframelabel = Label(RegisterFrame, text="", font=('times', 18))
        registerframelabel.grid(row=5, columnspan=2)

        #Label creation for labels pertaining to register data
        username = Entry(RegisterFrame, font=('arial', 20), width=15)
        username.grid(row=1, column=1)
        password = Entry(RegisterFrame, font=('arial', 20), width=15, show="*")
        password.grid(row=2, column=1)
        firstname = Entry(RegisterFrame, font=('arial', 20), width=15)
        firstname.grid(row=3, column=1)
        lastname = Entry(RegisterFrame, font=('arial', 20), width=15)
        lastname.grid(row=4, column=1)

        btn_login = Button(RegisterFrame, text="Register", font=('arial', 18), width=35, command=registerf)
        btn_login.grid(row=6, columnspan=2, pady=20)

        fv.mainloop()

    #Creating buttons for login, Reset and register and exit.
    Button(mframe, text="login", height="2", width=10, command=login).place(x=100, y=250)
    Button(mframe, text="Reset", height="2", width=10, command=reset).place(x=300, y=250)
    Button(mframe, text="exit", height="2", width=7, ).place(x=500, y=250)
    Button(mframe, text="register", height="2", width=10, command=register).place(x=600, y=250)

    loginscreen.mainloop()

mainloginscree()
