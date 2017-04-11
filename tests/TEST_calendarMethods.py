import sys
import unittest
sys.path.append("../src/scheduler")
from calendarMethods import *
from clientID_clientSecret import CLIENT_ID , CLIENT_SECRET
#need to import refresh token aswell
class massageItslearningDataTester(unittest.TestCase):

    def test_getAllUserReffreshTokens_correctInput(self):
    	correctReturnValue= False
        stringStudentID = "TDT4140"
    	self.assertEqual(getAllUserReffreshTokens(stringStudentID,correctReturnValue))

    def test_ofsetDateByANumberOfDays_correct_input(self):
    	correctReturnValue= "2017-03-22"
        inDate = "2017-03-19"
        ofset = 3
    	self.assertEqual(ofsetDateByANumberOfDays(inDate,ofset),correctReturnValue)

    def test_getDayEvents_correct_input(self):
    	date= "2017-03-22"
        time = "23:59:59"
        ofset = 1
        correctReturnValue = "findEventHere"
        http = authorise(CLIENT_ID,CLIENT_SECRET,refreshToken)
    	self.assertEqual(getDayEvents(date,time,ofset,http),correctReturnValue)
    
    def test_createAndExecuteEvent(self):
    	tittel="Test"
    	startdato="2017-04-10"
    	sluttdato="2017-04-10"
    	starttid="23:59:58"
    	sluttid="23:59:59"
    	beskrivelse="Test"
    	sted="Oslo"
    	colorId="1"
    	http=authorise(CLIENT_ID,CLIENT_SECRET,refreshToken)
    	self.assertEqual(getDayEvents(date,time,ofset,http),correctReturnValue)
  


