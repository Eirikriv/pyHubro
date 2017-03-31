import sys
import unittest

sys.path.append("../src/controller")
from scrapeController import *

class calendarControllerTester(unittest.TestCase):
    #Testing the first function in scrapeController
    def test_scanForLecturesInCourseAndInsert_Wrong_Input(self):
    	inputToTest = ["","012","!=V!FG","E",None]
    	correctOutput = None
    	for entry in inputToTest:
    		self.assertEqual(getLecturesAndInsertIntoCalendar(entry)[2],correctOutput)
    def test_scanForLecturesInCourseAndInsert__Correct_Input(self):
    	inputToTest = []#Insert correct coursecode, year and spring here 
    	correctOutput = 0
    	for entry in inputToTest:
    		self.assertEqual(getLecturesAndInsertIntoCalendar(entry)[1],correctOutput)
    
    #Testing the secound function in scrapeController
    def test_scanForAssignmentInACourseAndInsert_Wrong_Input(self):
        inputToTest = ["","012","!=V!FG","E",None]
        correctOutput = 0
        for entry in inputToTest:
            self.assertEqual(getLecturesAndInsertIntoCalendar(entry)[0],correctOutput)
    
    def test_scanForAssignmentInACourseAndInsert__Correct_Input(self):
        inputToTest = []#Insert correct coursecode, year and spring here 
        correctOutput = 0 
        for entry in inputToTest:
            self.assertEqual(getLecturesAndInsertIntoCalendar(entry)[1],correctOutput)