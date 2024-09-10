1. Student Table:
   - Stu_ID: Primary Key
   - Stu_Name
   - Wel_Mes
   - Email
   - Password
2. Behaviour Table:
   - Beh_ID: Primary Key
   - Stu_ID: Foreign key
   - Log_T
   - Dur
3. Timetable Table:
   - Tt_ID: Primary Key
   - Stu_ID: Foreign key
   - Day
   - Start_Time
   - End_Time
   - Cour_ID: Foreign key
4. Course Table:
   - Cour_ID: Primary Key
   - Cour_Name
   - Cour_Adr
5. Course_Link Table:
   - Link_ID: Primary Key
   - Course_ID: Foreign key
   - Link_Type: Zoom, tutorial/lecture notes, message, etc.
   - Link
