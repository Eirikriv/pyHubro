import sys
import unittest

sys.path.append("../src/controller")
from calendarController import *

class calendarControllerTester(unittest.TestCase):
    #Testing the first function in calendarController
    def test_getLecturesAndInsertIntoCalendar_Wrong_Input(self):
    	inputToTest = ["","012","!=V!FG","E",None]
    	correctOutput = False
    	for entry in inputToTest:
    		self.assertEqual(getLecturesAndInsertIntoCalendar(entry),correctOutput)
    def test_getLecturesAndInsertIntoCalendar_Correct_Input(self):
    	inputToTest = []#Insert correct studentIDs here 
    	correctOutput = True
    	for entry in inputToTest:
    		self.assertEqual(getLecturesAndInsertIntoCalendar(entry),correctOutput)
    
    #Testing the secound function in calendarController
	def test_getassignmentDeadLineAndInsertIntoCalendar_Wrong_Input(self):
    	inputToTest = ["","1441","!'=V!FG'","'1E1'",None]
    	correctOutput = False
    	for entry in inputToTest:
    		self.assertEqual(getLecturesAndInsertIntoCalendar(entry),correctOutput)
    def test_getassignmentDeadLineAndInsertIntoCalendar_Correct_Input(self):
    	inputToTest = []#insert correct studentIDs here
    	correctOutput = True
    	for entry in inputToTest:
    		self.assertEqual(getLecturesAndInsertIntoCalendar(entry),correctOutput)
	
	#Testing the secound function in calendarController
	def test_useHubroToFindTimeSlotsForAssignments_Wrong_Input(self):
    	inputToTest = ["","1441","!'=V!FG'","'1E1'",None]
    	correctOutput = False
    	for entry in inputToTest:
    		self.assertEqual(getLecturesAndInsertIntoCalendar(entry),correctOutput)
    def test_useHubroToFindTimeSlotsForAssignments_Correct_Input(self):
    	inputToTest = []#insert correct studentIDs here
    	correctOutput = True
    	for entry in inputToTest:
    		self.assertEqual(getLecturesAndInsertIntoCalendar(entry),correctOutput)

if __name__ == '__main__':
    unittest.main()
