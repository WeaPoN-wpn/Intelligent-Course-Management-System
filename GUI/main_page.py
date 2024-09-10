from tkinter import *
from PIL import ImageTk, Image 
import mysql.connector
import PySimpleGUI as sg
import cv2
import pickle
from datetime import datetime
import sys

# connect mysql server
myconn = mysql.connector.connect(host="localhost", user="root", passwd="20020429", database="facerecognition")
cursor = myconn.cursor()


# ------------------- face recognition ----------------------

# Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_rec/train.yml")

labels = {"person_name": 1}
with open("face_rec/labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('face_rec/haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

def recognize_user(timeout=40, confidence_threshold=80, gui_confidence=80):
    start_time = datetime.now()
    win_started = False
    win = None  # Initialize win variable

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            id_, conf = recognizer.predict(roi_gray)

            if conf >= gui_confidence:
                name = labels[id_]
                current_name = name

                select = "SELECT student_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Student WHERE name='%s'" % (name)
                name = cursor.execute(select)
                result = cursor.fetchall()
                data = "error"

                for x in result:
                    data = x

                if data != "error":
                    if win:  # Check if win is not None before calling Close
                        win.Close()
                        win = None
                    cap.release()
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

# ----------------- face recognition end --------------------

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
        
    def face_reg(self):
        self.login.place_forget()
        user_identity = recognize_user()
        cap.release()
        if user_identity:
            print("login successful")
            # Hide the previous interface
            self.bg_panel.place_forget()
            self.login_success = Label(self.window, text="welcome sb")
            self.login_success.place(x=500,y=500)

            # Create a new Frame for your new interface
            self.new_interface = Frame(self.window)
            self.new_interface.place(x=0, y=0)

            Label(self.new_interface, text="This is the new interface").pack()

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
        name = self.username_entry.get()
        input_password = self.password_entry.get()
        
        # p_command is used to find the password from the MySQL server based on the username 
        p_command = "SELECT password FROM user WHERE username = '%s'" % (name)
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
            print("WELCOME, %s" % (name))
            
#以下是插入函数内容
from tkinter import *
from PIL import ImageTk, Image 
import mysql.connector

# connect mysql server
myconn = mysql.connector.connect(host="localhost", user="root", passwd="82200036", database="sample_data")
cursor = myconn.cursor()

class MoodlePage:
    # ... other methods remain unchanged ...

    def submit_login(self):
        # this is the password of the user input
        name = self.username_entry.get()
        input_password = self.password_entry.get()
        
        # p_command is used to find the password from the MySQL server based on the username 
        p_command = "SELECT password FROM user WHERE username = '%s'" % (name)
        password_database = cursor.execute(p_command)
        result = cursor.fetchone()
        
        if result is not None:
            password_database = result[0]
        else:
            password_database = None

        if password_database is None:
            print("username not found, please check your input")

        if input_password == password_database:
            print("WELCOME, %s" % (name))
            self.create_new_moodle_page()  # Call the new method after login success
        else:
            print('''The Password input is not valid...
            please try again...''') 

    def create_new_moodle_page(self):
        # Hide the previous interface
        for widget in self.window.winfo_children():
            widget.place_forget()

        # Add the class buttons to the new interface
        Button(self.window, text="class1", command=self.open_class1).place(x=100, y=100)
        Button(self.window, text="class2", command=self.open_class2).place(x=200, y=100)
        Button(self.window, text="class3", command=self.open_class3).place(x=300, y=100)

    # Add methods to handle button clicks
    def open_class1(self):
        print("Opening class1...")

    def open_class2(self):
        print("Opening class2...")

    def open_class3(self):
        print("Opening class3...")


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