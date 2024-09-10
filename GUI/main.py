import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image 
import mysql.connector
import PySimpleGUI as sg
import cv2
import pickle
from datetime import datetime
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import webbrowser

# connect mysql server
myconn = mysql.connector.connect(host="localhost", user="root", passwd="108817", database="facerecognition")
cursor = myconn.cursor()


# plot time table 
def create_timetable_figure(student_id):
    # Establish a connection to the MySQL database
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="108817",
        database="facerecognition"
    )

    # Create a cursor object
    db_cursor = db_connection.cursor()

    # SQL query to get timetable for a specific student
    query = f"""
    SELECT Day, Start_Time, End_Time, Cour_Name 
    FROM Timetable 
    JOIN Course ON Timetable.Cour_ID = Course.Cour_ID 
    WHERE Stu_ID = {student_id};
    """

    # Execute the query
    db_cursor.execute(query)

    # Fetch all the rows
    timetable_data = db_cursor.fetchall()

    # Close the database connection
    db_cursor.close()
    db_connection.close()

    # Plotting
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    fig = plt.Figure(figsize=(10,5.89))
    ax = fig.add_subplot(1,1,1)

    for row in timetable_data:
        day, start_time, end_time, course_name = row
        day_index = days_of_week.index(day)
        start = start_time.seconds / 3600  # Convert seconds to hours
        end = end_time.seconds / 3600  # Convert seconds to hours

        # plot event
        ax.fill_between([day_index, day_index+1], [start, start], [end,end], edgecolor='k', linewidth=0.5)
        # plot beginning time
        ax.text(day_index+0.1, start+0.1 ,'{0}:{1:0>2}'.format(int(start),int((start*60)%60)), va='top', fontsize=7)
        # plot event name
        ax.text(day_index+0.5, (start+end)*0.5, course_name, ha='center', va='center', fontsize=11)

    # Set Axis
    ax.yaxis.grid()
    ax.set_xlim(0, len(days_of_week))
    ax.set_ylim(9, 19)  # 9:00 AM to 7:00 PM (in 24-hour format)
    ax.set_xticks(np.arange(len(days_of_week)))
    ax.set_xticklabels(days_of_week)
    ax.set_yticks(np.arange(9, 20))  # Hourly ticks
    ax.set_yticklabels(['{0}:00'.format(i) for i in range(9, 20)])  # Convert to time format
    ax.set_ylabel('Time')

    return fig 

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
        
    def recognize_user(self,timeout=40, confidence_threshold=80, gui_confidence=80):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("face_rec/train.yml")

        labels = {"person_name": 1}
        with open("face_rec/labels.pickle", "rb") as f:
            labels = pickle.load(f)
            labels = {v: k for k, v in labels.items()}

        # Define camera and detect face
        face_cascade = cv2.CascadeClassifier('face_rec/haarcascade/haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)
        
        start_time = datetime.now()
        win_started = False
        win = None  # Initialize win variable

        while True:
            ret, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                id_, conf = recognizer.predict(roi_gray)

                if conf >= gui_confidence:
                    name = labels[id_]
                    self.user_name = name

                    select = "SELECT Stu_ID FROM Student WHERE Stu_Name='%s'" % (name)
                    name = cursor.execute(select)
                    result = cursor.fetchall()
                    data = "error"

                    for x in result:
                        data = x

                    if data != "error":
                        if win:  # Check if win is not None before calling Close
                            win.Close()
                            win = None
                        self.cap.release()
                        cv2.destroyAllWindows()
                        return True

                else:
                    color = (255, 0, 0)
                    stroke = 2
                    font = cv2.QT_FONT_NORMAL
                    cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            imgbytes = cv2.imencode('.png', frame)[1].tobytes() 
            if not win_started:
                win_started = True
                layout = [
                    [sg.Text('Moodle Login Page', size=(30,1))],
                    [sg.Image(data=imgbytes, key='_IMAGE_')],
                    [sg.Exit()]
                ]
                win = sg.Window('Moodle Login Page',
                        default_element_size=(14, 1),
                        text_justification='right',
                        auto_size_text=False).Layout(layout).Finalize()
                image_elem = win.FindElement('_IMAGE_')
            else:
                event, values = win.Read(timeout=20)
                # Check if window is closed by the user
                if event == sg.WINDOW_CLOSED or event == 'Exit':
                    if win:  # Check if win is not None before calling Close
                        win.Close()
                        win = None
                    return False
                image_elem.Update(data=imgbytes)

            elapsed_time = datetime.now() - start_time
            if elapsed_time.seconds > timeout:
                print("User not recognized within timeout")
                if win:  # Check if win is not None before calling Close
                    win.Close()
                return False

        if win:  # Check if win is not None before calling Close
            win.Close()
        return False
    
    
        
    def face_reg(self):
        self.login.place_forget()
        user_identity = self.recognize_user()
        self.cap.release()
        if user_identity:
            self.time = datetime.now()
            self.now = self.time.strftime('%Y-%m-%d %H:%M:%S')
            #### get the user _id #####
            query1 = "SELECT Stu_ID FROM student WHERE Stu_Name=%s"
            cursor.execute(query1, (self.user_name,))
            student_id_result = cursor.fetchall()
            self.stu_id = student_id_result[0][0]
            
            ###########################
            print("login successful")
            print("hello",self.user_name)
            # Hide the previous interface
            self.conditional_create()

        else:
            self.require_username = Label(self.window,text="please login with username and password")
            self.require_username.place(x=850,y=450)
            self.require_permit = Button(self.window, text="ok",command=self.show_login_form)
            self.require_permit.place(x=850,y=500)
            

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
        self.user_name = self.username_entry.get()
        input_password = self.password_entry.get()
        
        # p_command is used to find the password from the MySQL server based on the username 
        p_command = "SELECT password FROM Student WHERE Stu_Name = '%s'" % (self.user_name)
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
            print("WELCOME, %s" % (self.user_name))
            #以下是插入函数内容
            query1 = "SELECT Stu_ID FROM student WHERE Stu_Name=%s"
            cursor.execute(query1, (self.user_name,))
            student_id_result = cursor.fetchall()
            self.stu_id = student_id_result[0][0]
            
            self.conditional_create()
        else:
            print("Wrong")
            
    ###################### 弹窗 ####################################
    def create_window(self):
        new_window = tk.Toplevel(self.window)
        new_window.geometry("230x200+750+400")  # 窗口大小为200x200，
        new_window.overrideredirect(1)  # Removes window decorations, making the window unresizable
        new_window.attributes('-topmost', 1)  # Set the new window on top of all other windows
        label = tk.Label(new_window, text="You have class within one hour")
        label.place(x=20,y=80)
        button = tk.Button(new_window, text="Click me")
        button.place(x=85, y=170)
        
    def conditional_create(self):
        condition = self.have(self.stu_id)
        
        if condition:
            self.create_new_moodle_page(self.stu_id)
            self.create_window()
        else:
            self.create_new_moodle_page(self.stu_id)
    
    ################################################################
            
    def have(self,stu_id):
    # 查询一小时内是否有课程
        now = datetime.now()
        one_hour_later = now + timedelta(hours=1)   
        now_str = now.strftime('%H:%M:%S')
        one_hour_later_str = one_hour_later.strftime('%H:%M:%S')
        query = f"""
        SELECT * FROM Timetable
        WHERE Stu_ID = {stu_id}
        AND Start_Time >= '{now_str}'
        AND Start_Time <= '{one_hour_later_str}';
        """
        cursor.execute(query)

        # 获取查询结果
        result = cursor.fetchall()

        # 如果结果不为空，则表示一小时内有课程
        if result:
            
            return True 
        else:
            
            return False
    ######################################################################
            
    def create_new_moodle_page(self,stu_id):
        # Hide the previous interface
        have_class = self.have(stu_id)
        for widget in self.window.winfo_children():
            widget.place_forget()
        user_name = self.user_name
        # Add the class buttons to the new interface
        have_class = True
        select_class = ""
        if have_class:
            # 左边按钮 右边课表
            # 多加一个弹窗
            query = '''
            SELECT Distinct Course.Cour_Name
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
                Button(self.window, text=course[0], command=lambda: self.open_course(course_name=course[0])).place(x=x, y=y)
                y += 100
                
            
            # show class time table 
            query1 = "SELECT Stu_ID FROM student WHERE Stu_Name=%s"
            cursor.execute(query1, (user_name,))
            student_id_result = cursor.fetchall()
            student_id = student_id_result[0][0]
            fig = create_timetable_figure(student_id)
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().place(x=700,y=200)
            
        else:
            # 左边按钮 右边课表
            query = '''
            SELECT Distinct Course.Cour_Name
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
                Button(self.window, text=course[0], command=lambda: self.open_course(course_name=course[0])).place(x=x, y=y)
                y += 100
                
            
            # show class time table 
            query1 = "SELECT Stu_ID FROM student WHERE Stu_Name=%s"
            cursor.execute(query1, (user_name,))
            student_id_result = cursor.fetchall()
            student_id = student_id_result[0][0]
            fig = create_timetable_figure(student_id)
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().place(x=700,y=200)

    def open_link(self, link):
        # 打开链接
        webbrowser.open(link)

    def open_course(self,course_name):
        # Handle the button click event for opening a course
        email_link = 'https://outlook.office.com/mail/'
        zoom_link_query = "SELECT Zoom_Link FROM Zoom_Link INNER JOIN Course ON Zoom_Link.Cour_ID = Course.Cour_ID WHERE Course.Cour_Name = '%s'" % course_name
        lec_note_query = "SELECT LNote_Link FROM Lec_Note INNER JOIN Course ON Lec_Note.Cour_ID = Course.Cour_ID WHERE Course.Cour_Name = '%s'" % course_name
        tut_note_query = "SELECT TNote_Link FROM Tut_Note INNER JOIN Course ON Tut_Note.Cour_ID = Course.Cour_ID WHERE Course.Cour_Name = '%s'" % course_name
        syllabus_query = "SELECT Syb_Link FROM Syllabus INNER JOIN Course ON Syllabus.Cour_ID = Course.Cour_ID WHERE Course.Cour_Name = '%s'" % course_name

        ## 课程信息,用于输出label
        info_query = "SELECT Cour_Name, Cour_Adr FROM Course WHERE Course.Cour_Name = '%s'" % course_name
        
        cursor.execute(zoom_link_query)
        zoom_link = cursor.fetchone()[0] # Assuming there is only one Zoom link per course

        cursor.execute(lec_note_query)
        lec_note_link = cursor.fetchone()[0] # Assuming there is only one lecture note link per course

        cursor.execute(tut_note_query)
        tut_note_link = cursor.fetchone()[0] # Assuming there is only one tutorial note link per course

        cursor.execute(syllabus_query)
        syllabus_link = cursor.fetchone()[0] # Assuming there is only one syllabus link per course

        cursor.execute(info_query)
        info_text = cursor.fetchone()[0] # Assuming there is only one message per course

        # Hide the previous interface
        for widget in self.window.winfo_children():
            widget.place_forget()

        # Generate buttons for Zoom Link, Lecture Note, Tutorial Note, Syllabus, and Message
        x = 100
        y = 100

        Button(self.window, text="Course_info_link", command=lambda: self.open_link(syllabus_link)).place(x=x, y=y)
        y += 100

        Button(self.window, text="Zoom_link", command=lambda: self.open_link(zoom_link)).place(x=x, y=y)
        y += 100

        Button(self.window, text="Lecture_note", command=lambda: self.open_link(lec_note_link)).place(x=x, y=y)
        y += 100

        Button(self.window, text="Tutorial_note", command=lambda: self.open_link(tut_note_link)).place(x=x, y=y)
        y += 100

        Button(self.window, text="Send_email", command=lambda: self.open_link(email_link)).place(x=x, y=y)



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