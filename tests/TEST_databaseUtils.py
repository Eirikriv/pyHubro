import sys
import unittest
sys.path.append("../src/databasehandler")
from databaseUtils import *

class massageItslearningDataTester(unittest.TestCase):
    engine = create_engine(URI)
    connection = engine.connect()
    
    def test_getEntryFromStudentTable_Correct_Input(self):
        inputToTest = #Find correct studentID
        correctOutput = #Corresponding row from database
        for entry in inputToTest:
            self.assertEqual(getEntryFromStudentTable(engine,connection,inputToTest),correctOutput)

    def test_getEntriesFromStudent_courseTable_Correct_Input(self):
        inputToTest = #Find correct studentID
        correctOutput = #Corresponding row from database
        for entry in inputToTest:
            self.assertEqual(getEntriesFromStudent_courseTable(engine,connection,inputToTest),correctOutput)

    def test_insertACourseIntoDatabase_courseTable_Correct_Input(self):
        inputToTest = ["TDT4140","System engeneering"]
        correctOutput = ["TDT4140","System engeneering"]
        for entry in inputToTest:
            self.assertEqual(getEntriesFromStudent_courseTable(engine,connection,inputToTest[0],inputToTest[1]),correctOutput[0])

    def test_getEntriesFromCourseTable_courseTable_Correct_Input(self):
        inputToTest = "TDT4140"
        correctOutput = ["TDT4140","System engeering"]
        for entry in inputToTest:
            self.assertEqual(getEntriesFromCourseTable(engine,connection,inputToTest)[0],correctOutput[0])

    def test_getEntryFromLectureTable_correctInsert(self):
        lectureID="TDT4140-2017-12-20-23:59:00"
        lectureDate= "2017-12-20"
        lectureTime= "23:59:00"
        insertAssignmnentIntoDatabase(lectureID,lectureDate,lectureTime)
        self.assertEqual(getEntryFromLectureTable(assignmentID),(assignmentID, assignmnentDate,assignmnentTime))
#got here in testing databaseclases
    def test_getEntriesFromLectureTable_courseTable_Correct_Input(self):
        inputToTest = "TDT4140001"
        correctOutput = #output from assignmentTable
        for entry in inputToTest:
            self.assertEqual(getEntriesFromLectureTable(engine,connection,inputToTest),correctOutput)
 
    def test_insertLecturesIntoDatabase_courseTable_Correct_Input(self):
        inputToTest = "TDT4140001"
        correctOutput = #output from assignmentTable
        for entry in inputToTest:
            self.assertEqual(getEntriesFromCourseTable(engine,connection,inputToTest),correctOutput)
    
    def test_insertLecture_courseIntoDatabase_courseTable_Correct_Input(self):
        inputToTest = ["TDT4140001","TDT4140"]
        correctOutput = ["TDT4140001","TDT4140"]#output from assignmentTable
        insertLecture_courseIntoDatabase(engine, connection, inputToTest[0],inputToTest[1])
        for entry in inputToTest:
            self.assertEqual(getEntryFromLecture_courseTable(engine,connection,inputToTest[0]),["TDT4140001","TDT4140"])
    
    def test_getEntryFromLecture_courseTable_Correct_Input(self):
        inputToTest = ["TDT4140001","TDT4140"]
        correctOutput = ["TDT4140001","TDT4140"]#output from assignmentTable
        insertLecture_courseIntoDatabase(engine, connection, inputToTest[0],inputToTest[1])
        for entry in inputToTest:
            self.assertEqual(getEntryFromLecture_courseTable(engine,connection,inputToTest[0]),["TDT4140001","TDT4140"])
    
    def test_getEntriesFromAssignment_courseTableReturnAssignments_Correct_Input(self):
        inputToTest = ""#Find correct studentIDs to test
        correctOutput = #list courses
        insertLecture_courseIntoDatabase(engine, connection, inputToTest[0],inputToTest[1])
        for entry in inputToTest:
            self.assertEqual(getEntriesFromAssignment_courseTableReturnAssignments(engine,connection,inputToTest[0]),["TDT4140001","TDT4140"])
  
    def test_getEntryFromAssignmentStudentInitialHoursForStudent_courseTableReturnAssignments_Correct_Input(self):
        inputToTest = ""#Find correct studentIDs to test
        correctOutput = #list courses
        insertLecture_courseIntoDatabase(engine, connection, inputToTest[0],inputToTest[1])
        for entry in inputToTest:
            self.assertEqual(getEntryFromAssignmentStudentInitialHoursForStudent(engine,connection,inputToTest[0]),["TDT4140001","TDT4140"])
    
    def test_getAllEntriesFromStudentTable_Correct_Input(self):
        inputToTest = ""#Find correct studentIDs to test
        correctOutput = #list courses
        insertLecture_courseIntoDatabase(engine, connection, inputToTest[0],inputToTest[1])
        for entry in inputToTest:
            self.assertEqual(getAllEntriesFromStudentTable(engine,connection,inputToTest[0]),["TDT4140001","TDT4140"])

    def test_getEntryFromStudentSetting_Correct_Input(self):
        inputToTest = ""#Find correct studentIDs to test
        correctOutput = #list studentSettings
        self.assertEqual(getEntryFromStudentSetting(engine,connection,inputToTest[0]),["TDT4140001","TDT4140"])
    

if __name__ == '__main__':
    unittest.main()