import sys
import unittest
sys.path.append("../src/scraper")
from loginAndScrapeBlackBoard import *

class loginAndScrapeBlackBoard(unittest.TestCase):
	
	def test_getUsername_Correct_Input(self):
        correctOutput = "helenehs"#Corresponding row from database
        self.assertEqual(getUsername(),correctOutput)
    
    def test_scrapeBlackBoard_correct_input():
    	correctOutput = []
    	self.assertEqual(scrapeBlackBoard(0),correctOutput)
    
    def test_isNumber_correctInput():
    	test_input = "2"
    	correctOutput = True
    	self.assertEqual(isNumber(test_input),correctOutput)
    
    def test_getDateOnRightFormat_sample_days_correct(self):
        days = ["01","31","15",".7",".3","12.","03"]
        correctDays=["01","31","15","07","03","12","03"]
        for n in range(len(days)-1):
            self.assertEqual(getDateOnRightFormat(days[n]),correctDays[n])
    
    def test_parceFromBlackBoardToDatabase():
    	test_input = [[],[]]
    	correctOutput = [[],[]]
    	for n in correctOutput:
    		self.assertEqual(parceFromBlackBoardToDatabase(test_input),correctOutput)
    
    def test_mounthConverter_correct_input():
    	test_input = "Mar"
    	correctOutput= "03"
    	self.assertEqual(monthConverter(test_input),correctOutput)

    def test_convertTimeToRightFormate_correct_input():
    	test_input = "Mar"
    	correctOutput= "03"
    	self.assertEqual(monthConverter(test_input),correctOutput)

if __name__ == '__main__':
    unittest.main()	