from tkinter import *
from PIL import ImageTk, Image 
import mysql.connector
import PySimpleGUI as sg
import cv2
import pickle
from datetime import datetime
import sys
from tabulate import tabulate

# connect mysql server
myconn = mysql.connector.connect(host="localhost", user="root", passwd="20020429", database="gp")
cursor = myconn.cursor()



# ------------------------- gui -----------------------------
class MoodlePage:
    def __init__(self, window):

        # window 是我们这个窗口的名称，后续代码也请保持一致，避免重新打开新窗口
        self.window = window 
        self.window.geometry("1116x718")
        self.window.resizable(0,0)
        self.window.state("zoomed")
        self.window.title("Moodle Login Page")
        self.window.configure(bg="white")

        # background pic

        self.bg_frame = Image.open("moodle.png")
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo, bg="white")
        self.bg_panel.image = photo
        self.bg_panel.place(x=400, y=30)


        # login button, the design is after the login button is clicked, face_rec will then start
        self.login = Button(self.window, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=1,
                            bg='white', activebackground='white', fg='black', command=self.face_reg)
        self.login.place(x=750, y=450)  


    def show_login_form(self):
        self.login.place_forget()
        self.require_permit.place_forget()
        self.require_username.place_forget()

        # Create username label and text entry box
        self.username_input = Label(self.window, text="Username")
        self.username_input.place(x=750, y=400)
        self.username_entry = Entry(self.window)
        self.username_entry.place(x=850, y=400)

        # Create password label and text entry box
        self.input_password = Label(self.window, text="Password")
        self.input_password.place(x=750, y=450)
        self.password_entry = Entry(self.window, show='*')
        self.password_entry.place(x=850, y=450)

        # submit button, after clicking will verify the user 
        Button(self.window, text="Submit", command=self.submit_login).place(x=850, y=500)

    def submit_login(self):
        # this is the password of the user input
        self.name = self.username_entry.get()
        input_password = self.password_entry.get()
        
        # p_command is used to find the password from the MySQL server based on the username 
        p_command = "SELECT password FROM Student WHERE Stu_Name = '%s'" % (self.name)
        password_database = cursor.execute(p_command)
        result = cursor.fetchone()
        
        if result is not None:
            password_database = result[0]
        else:
            password_database = None
        # insert one record
        # INSERT INTO user (id, username, password) VALUES (1,'vfzzz', '123456');

        # need to ensure the print function will appear on the window 

        if password_database == None:
            print("username not found, please check your input")

        if input_password == password_database:
            print("WELCOME, %s" % (self.name))
            #以下是插入函数内容
            self.create_new_moodle_page()
            
    

    def create_new_page_without_class(self):
        # Hide the previous interface
        for widget in self.window.winfo_children():
            widget.place_forget()
        user_name = self.name

        query = '''
            SELECT timetable.`Day`, course.Cour_Name, timetable.Start_Time, timetable.End_Time
            FROM timetable
            JOIN student ON timetable.Stu_ID = student.Stu_ID
            JOIN course ON timetable.Cour_ID = course.Cour_ID
            WHERE student.Stu_Name = %s
        '''
        cursor.execute(query, (user_name,))

        rows = cursor.fetchall()

        # Get the column names
        column_names = [i[0] for i in cursor.description]

        # Use tabulate to print the result in a table format
        print(tabulate(rows, headers=column_names, tablefmt='pipe'))
            
    def create_new_moodle_page(self):
        # Hide the previous interface
        for widget in self.window.winfo_children():
            widget.place_forget()
        user_name = self.name
        # Add the class buttons to the new interface
        have_class = True
        select_class = ""
        if have_class:
            # 左边按钮 右边课表
            # 多加一个弹窗
            query = '''
            SELECT Course.Cour_Name
            FROM Timetable
            INNER JOIN Student ON Timetable.Stu_ID = Student.Stu_ID
            INNER JOIN Course ON Timetable.Cour_ID = Course.Cour_ID
            WHERE Student.Stu_Name = %s
            '''
            cursor.execute(query,(user_name,))
            courses = cursor.fetchall()

            # Generate buttons for each course
            x = 100
            y = 100
            for course in courses:
                Button(self.window, text=course[0], command=self.open_course).place(x=x, y=y)
                y += 100
        else:
            # 左边按钮 右边课表
            ...
    def open_course(self):
        # Handle the button click event for opening a course
        pass
    
            
    # Add methods to handle button clicks

    def page():
        ...
        """
        else:
            print('''The Password input is not valid...
            please try again...''') 
        """


def on_window_close(event):
        sys.exit()

window = Tk()
app = MoodlePage(window)
window.bind("<Destroy>", on_window_close)
window.mainloop()
