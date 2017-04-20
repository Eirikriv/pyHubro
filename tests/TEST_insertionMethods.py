import sys
sys.path.append("../src/databasehandler")
from insertionMethods import *
import unittest    

class insertionMethodTester(unittest.TestCase):
    
    engine = None
    connection = None
    try:
        engine = create_engine(URI)
        connection = engine.connect()
    except:
        None


    def test_insertLectureIntoDatabase_correctInsert(self):
        correctReturnValue= False
        lectureID="0008"
        lectureDate= "2017-12-20"
        lectureStartTime= "08:15:00"
        lectureEndTime ="10:00:00"
        lectureDescription="Lecture in TDT 4140"
        lectureLocation="R1"
        self.assertEqual(insertLectureIntoDatabase(insertionMethodTester.engine,insertionMethodTester.connection,lectureID,lectureDate,lectureStartTime,lectureEndTime,lectureDescription,lectureLocation),correctReturnValue)

    def test_insertCourseIntoDatabase_correctInput(self):
        correctReturnValue= False
        stringCourseID = "TDT4140"
        stringCourseName = "TDT4140"
        self.assertEqual(insertCourseIntoDatabase(insertionMethodTester.engine,insertionMethodTester.connection,stringCourseID, stringCourseName),correctReturnValue)
    
    def test_insertAnAssignmentIntoDatabase_correctInput(self):
        correctReturnValue= False
        stringAssignmnentID = "TDT4140"
        stringAssignmnentDate = "2017-03-22"
        stringAssignmnentTime = "23:59:00" 
        stringAssignmentDescription = "Sprint Delivery 3 PU"
        self.assertEqual(insertAnAssignmentIntoDatabase(insertionMethodTester.engine,insertionMethodTester.connection,stringAssignmnentID, stringAssignmnentDate,stringAssignmnentTime,stringAssignmentDescription),correctReturnValue)        
    
    def test_insertLectureCourseIntoDatabase_correctInsert(self):
        correctReturnValue= False
        lectureID = "0008"
        courseID = "TDT4100" 
        self.assertEqual(insertLectureCourseIntoDatabase(insertionMethodTester.engine,insertionMethodTester.connection,lectureID,courseID),correctReturnValue)

    def test_getValueFromCourseTable_correctInput(self):
        correctReturnValue= False
        stringCourseID = "TDT4140"
        self.assertEqual(getValueFromCourseTable(insertionMethodTester.engine,insertionMethodTester.connection,stringCourseID),correctReturnValue)     
    
    def test_getALectureFromLectureTable_correctInput(self):
        correctReturnValue= False
        stringLectureID = "TDT4140001"
        self.assertEqual(getALectureFromLectureTable(insertionMethodTester.engine,insertionMethodTester.connection,stringLectureID),correctReturnValue)     

    def test_getValueFromCourseTable_correctInput(self):
        correctReturnValue= False
        stringCourseID = "TDT4140"
        self.assertEqual(getValueFromCourseTable(insertionMethodTester.engine,insertionMethodTester.connection,stringCourseID),correctReturnValue)     
    
    def test_getStudentFromStudentTable_correctInput(self):
        correctReturnValue= False
        stringStudentID = "0129124"
        self.assertEqual(getStudentFromStudentTable(insertionMethodTester.engine,insertionMethodTester.connection,stringStudentID),correctReturnValue)     

    def test_getStudent_settingFromStudentTable_correctInput(self):
        correctReturnValue= False
        stringStudentID = "0129124"
        self.assertEqual(getStudent_settingFromStudentTable(insertionMethodTester.engine,insertionMethodTester.connection,stringStudentID),correctReturnValue)     

if __name__ == '__main__':
    unittest.main()  