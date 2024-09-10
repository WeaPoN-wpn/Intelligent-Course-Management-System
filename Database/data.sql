INSERT INTO Student (Stu_ID, Stu_Name, Wel_Mes, Email, Password)
VALUES
  (1, "John", "Welcome to WCUmoodle!", "john.doe@wcu.com", "password123");

INSERT INTO Behaviour (Beh_ID, Stu_ID, Log_T, Dur)
VALUES
  (1, 1, '2023-09-01 09:12:00', 120),
  (2, 1, '2023-09-02 14:30:00', 90),
  (3, 1, '2023-09-03 16:57:00', 60),
  (4, 1, '2023-09-04 10:15:00', 75);

INSERT INTO Course (Cour_ID, Cour_Name, Cour_Adr)
VALUES
  (1, "Mathematics", "Building A, Room 101"),
  (2, "Physics", "Building C, Room 303"),
  (3, "Computer Science", "Building E, Room 505");

INSERT INTO Timetable (Tt_ID, Stu_ID, Day, Start_Time, End_Time, Cour_ID)
VALUES
  (1, 1, "Monday", '11:30:00', '12:30:00', 1),
  (2, 1, "Tuesday", '14:00:00', '15:00:00', 3),
  (3, 1, "Wednesday", '18:00:00', '20:00:00', 2),
  (4, 1, "Thursday", '11:30:00', '13:30:00', 1),
  (5, 1, "Friday", '13:00:00', '15:00:00', 3);

INSERT INTO Zoom_Link (Zoom_ID, Cour_ID, Zoom_Link)
VALUES
  (1, 1, "https://example.com/course1/zoom"),
  (2, 2, "https://example.com/course2/zoom"),
  (3, 3, "https://example.com/course3/zoom");

INSERT INTO Lec_Note (LecNote_ID, Cour_ID, LNote_Link)
VALUES
  (1, 1, "https://example.com/course1/lecture-notes"),
  (2, 2, "https://example.com/course2/lecture-notes"),
  (3, 3, "https://docs.google.com/document/d/1NfCMNsEr9Z-ioIU9S_z_zIG89TCtP9gPSACqFobiT2U/edit?usp=sharing");

INSERT INTO Tut_Note (TutNote_ID, Cour_ID, TNote_Link)
VALUES
  (1, 1, "https://example.com/course1/tutorial-notes"),
  (2, 2, "https://example.com/course2/tutorial-notes"),
  (3, 3, "https://docs.google.com/document/d/1oacvdq90Psl4-S_05vIaeJRfxt_J_zCqjQmgSASEf2A/edit?usp=sharing");

INSERT INTO Syllabus (Syllabus_ID, Cour_ID, Syb_Link)
VALUES
  (1, 1, "https://example.com/course1/syllabus"),
  (2, 2, "https://example.com/course2/syllabus"),
  (3, 3, "https://example.com/course3/syllabus");

INSERT INTO Message (Message_ID, Cour_ID, Message_Text)
VALUES
  (1, 1, "Welcome to the Mathematics course!"),
  (2, 2, "Get ready for the Physics study this semester!"),
  (3, 3, "Introduction to programming in the Computer Science course.");
