-- Student Table
CREATE TABLE Student (
  Stu_ID INT PRIMARY KEY,
  Stu_Name VARCHAR(100),
  Wel_Mes VARCHAR(200),
  Email VARCHAR(100),
  Password VARCHAR(100)
);

-- Behaviour Table
CREATE TABLE Behaviour (
  Beh_ID INT PRIMARY KEY,
  Stu_ID INT,
  Log_T TIMESTAMP,
  Dur INT,
  FOREIGN KEY (Stu_ID) REFERENCES Student(Stu_ID)
);

-- Course Table
CREATE TABLE Course (
  Cour_ID INT PRIMARY KEY,
  Cour_Name VARCHAR(200),
  Cour_Adr VARCHAR(300)
);

-- Timetable Table
CREATE TABLE Timetable (
  Tt_ID INT PRIMARY KEY,
  Stu_ID INT,
  Day VARCHAR(50),
  Start_Time TIME,
  End_Time TIME,
  Cour_ID INT,
  FOREIGN KEY (Stu_ID) REFERENCES Student(Stu_ID),
  FOREIGN KEY (Cour_ID) REFERENCES Course(Cour_ID)
);

-- Zoom_Link Table
CREATE TABLE Zoom_Link (
  Zoom_ID INT PRIMARY KEY,
  Cour_ID INT,
  Zoom_Link VARCHAR(300),
  FOREIGN KEY (Cour_ID) REFERENCES Course(Cour_ID)
);

-- Lec_Note Table
CREATE TABLE Lec_Note (
  LecNote_ID INT PRIMARY KEY,
  Cour_ID INT,
  LNote_Link VARCHAR(300),
  FOREIGN KEY (Cour_ID) REFERENCES Course(Cour_ID)
);

-- Tut_Note Table
CREATE TABLE Tut_Note (
  TutNote_ID INT PRIMARY KEY,
  Cour_ID INT,
  TNote_Link VARCHAR(300),
  FOREIGN KEY (Cour_ID) REFERENCES Course(Cour_ID)
);

-- Syllabus Table
CREATE TABLE Syllabus (
  Syllabus_ID INT PRIMARY KEY,
  Cour_ID INT,
  Syb_Link VARCHAR(300),
  FOREIGN KEY (Cour_ID) REFERENCES Course(Cour_ID)
);

-- Message Table
CREATE TABLE Message (
  Message_ID INT PRIMARY KEY,
  Cour_ID INT,
  Message_Text VARCHAR(500),
  FOREIGN KEY (Cour_ID) REFERENCES Course(Cour_ID)
);
