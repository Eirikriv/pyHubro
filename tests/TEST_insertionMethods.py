import sys
sys.path.append("../src/databasehandler")

from

import unittest    
class massageItslearningDataTester(unittest.TestCase):

    def test_insertUserIntoDatabase_correctInsert(self):
        userName="Eirik Rivedal"
        userID= "1400"
        insertUserIntoDatabase(userID,userName)
        self.assertEqual(getEntryFromUserTable(userID),(userID, userName))
    def test_insertLectureIntoDatabase_correctInsert(self):
        lectureID="0008"
        lectureDate= "2017-12-20"
        lectureStartTime= "08:15:00"
        lectureEndTime ="10:00:00"
        lectureDescription="Lecture in TDT 4140"
        lectureLocation="R1"
        insertLectureIntoDatabase(lectureID,lectureDate,lectureStartTime,lectureEndTime,lectureDescription,lectureLocation)
        self.assertEqual(getEntryFromLectureTable(lectureID),(lectureID, lectureDate, lectureDescription, lectureLocation, lectureStartTime,lectureEndTime))

    def test_insertCourseIntoDatabase_correctInput(self):
        correctReturnValue= False
        stringCourseID = "TDT4140"
        stringCourseName = "TDT4140"
        self.assertEqual(insertCourseIntoDatabase(stringCourseID, stringCourseName),correctReturnValue)
    
    def test_insertAnAssignmentIntoDatabase_correctInput(self):
        correctReturnValue= False
        stringAssignmnentID = "TDT4140"
        stringAssignmnentDate = "2017-03-22"
        stringAssignmnentTime = "23:59:00" 
        stringAssignmentDescription = "Sprint Delivery 3 PU"
        self.assertEqual(insertAnAssignmentIntoDatabase(engine,connection,stringAssignmnentID, stringAssignmnentDate,stringAssignmnentTime,stringAssignmentDescription),correctReturnValue)        

    def test_insertLectureIntoDatabase_correctInput(self):
        correctReturnValue= False
        stringLectureID = "TDT4140"
        stringLectureDate = "2017-03-22"
        stringLectureStartTime = "08:15:00" 
        stringLectureEndTime = "10:00:00"
        stringDescription ="PU lecture"
        stringWhere  = "R1"
        self.assertEqual(insertLectureIntoDatabase(engine,connection,stringLectureID, stringLectureDate,stringLectureStartTime,stringLectureEndTime,stringDescription,stringWhere),correctReturnValue)        
    

    def test_getValueFromCourseTable_correctInput(self):
        correctReturnValue= False
        stringCourseID = "TDT4140"
        self.assertEqual(getValueFromCourseTable(engine,connection,stringCourseID),correctReturnValue)     
  
 