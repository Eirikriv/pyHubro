import sys
import unittest
sys.path.append("../src/scheduler")
sys.path.append("../src/databasehandler")
from calendarMethods import *
from clientID_clientSecret import CLIENT_ID , CLIENT_SECRET
#need to import refresh token aswell
class calendarMethods(unittest.TestCase):
    engine = None
    connection = None
    http = None
    try:
        engine = create_engine(URI)
        connection = engine.connect()
        refreshToken = getEntryFromStudentTable(calendarMethods.engine,calendarMethods.connection,"100867243925223857971")[4]
        http = authorise(CLIENT_ID,CLIENT_SECRET,refreshToken)
    except: 
        None
    def test_ofsetDateByANumberOfDays_correct_input(self):
    	correctReturnValue= "2017-03-22"
        inDate = "2017-03-19"
        ofset = 3
    	self.assertEqual(ofsetDateByANumberOfDays(inDate,ofset),correctReturnValue)

    def test_getDayEvents_correct_input(self):
    	date= "2017-03-22"
        time = "23:59:59"
        ofset = 1
        correctReturnValue = False
    	self.assertEqual(getDayEvents(date,time,ofset,calendarMethods.http),correctReturnValue)
    
    def test_createAndExecuteEvent(self):
    	tittel="Test"
    	startdato="2017-04-10"
    	sluttdato="2017-04-10"
    	starttid="23:59:58"
    	sluttid="23:59:59"
    	beskrivelse="Test"
    	sted="Oslo"
    	colorId="1"
        correctReturnValue = False
    	self.assertEqual(createAndExecuteEvent(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,colorId,calendarMethods.http),correctReturnValue)

if __name__ == '__main__':
    unittest.main()

