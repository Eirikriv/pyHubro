import sys
import unittest

sys.path.append("../src/controller")
sys.path.append("../src/scraper")
sys.path.append("../src/scheduler")
sys.path.append("../src/owlbrain")
sys.path.append("../src/databasehandler")
from scrapeController import *

class calendarControllerTester(unittest.TestCase):
    #Testing the first function in scrapeController
    def test_scanForLecturesInCourseAndInsert_Wrong_Input(self):
    	inputToTest = ["","012","!=V!FG","E",None]
    	correctOutput = None
    	for entry in inputToTest:
    		self.assertEqual(scanForLecturesInCourseAndInsert(entry,"2017","0")[2],correctOutput)
    
    #Testing the secound function in scrapeController
    def test_scanForAssignmentInACourseAndInsert_Wrong_Input(self):
        inputToTest = ["","012","!=V!FG","E",None]
        correctOutput = None
        for entry in inputToTest:
            self.assertEqual(scanForAssignmentInACourseAndInsert(entry),correctOutput)
    
if __name__ == '__main__':
    unittest.main()