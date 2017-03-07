
import sys

sys.path.append("../src/scraper")
sys.path.append("../src/databasehandler")
from massageItslearningData import *	
from readItslearningAssignments import *
from scrapeForCoursesItslearning import *
from clearDBConnect import *
import unittest

class massageItslearningDataTester(unittest.TestCase):
    def test_monthConverter_all_months_correct_number(self):
        months=["januar","februar","mars","april","mai","juni","juli","august","september","oktober","november","desember"]
        counter = 1
        for month in months:
            self.assertEqual(monthConverter(month), str(counter))
            counter +=1

    def test_monthConverter_wrong_month_format_error_flag(self):
        incorretcMonths=["jan", "feb" ,"January","Janu"]
        for incorretcMonth in incorretcMonths:
            self.assertEqual(monthConverter(incorretcMonth),"00")
    
    def test_getDateOnRightFormat_sample_days_correct(self): 
        days = ["01","31","15",".7",".3","12.","03"]
        correctDays=["01","31","15","07","03","12","03"]
    	for n in range(len(days)-1):
    		self.assertEqual(getDateOnRightFormat(days[n]),correctDays[n])

    def test_getDateOnRightFormat_sample_days_incorrect_flagg(self):
    	month = ["0112","3121","1415",".417",".13f",1,"abba","02","12"]
    	correcktMonth=["00","00","00","00","00","00","00","02","12"]
    	for n in range(len(month)-1):
    		self.assertEqual(getDateOnRightFormat(month[n]),correcktMonth[n])
    def test_isNumber(self):
        inList= ["1","s","+","@",",","3"]
        correctList=[True,False,False,False,False,True]
        for n in range(len(inList)):
            self.assertEqual(isNumber(inList[n]),correctList[n])

    def test_prepDeliveriesForDatabase_sample_scrape_correct(self):
        scrapeList =[['Assignment 2', 'TDT4300 DATAVAREH/DATAGRUVED V\xc5R 2017', 'Deadline: 10. mars 2017 08:00'], ['Assignment 2: Demonstrated learning of Core 1', 'TDT4140 PROGRAMVAREUTVIKL V\xc5R 2017', 'Deadline: 10. mars 2017 23:55'],['fsvsdv', 'zxce', 'D12fv']]
        correctList = [[' Assignment 2', ' TDT4300 DATAVAREH/DATAGRUVED', '2017-03-10', '08:00:00'], [' Assignment 2:', ' TDT4140 PROGRAMVAREUTVIKL', '2017-03-10', '23:55:00'],['', '', '00-00-00', '00:00:00']]
        for n in range(len(scrapeList)):
            self.assertEqual(prepDeliveriesForDatabase(scrapeList[n]),correctList[n])

    def test_prepAllDeiveriesForDatabase_sample_scrape_correct(self):
        scrapeList =[['Assignment 2', 'TDT4300 DATAVAREH/DATAGRUVED V\xc5R 2017', 'Deadline: 10. mars 2017 08:00'], ['Assignment 2: Demonstrated learning of Core 1', 'TDT4140 PROGRAMVAREUTVIKL V\xc5R 2017', 'Deadline: 10. mars 2017 23:55'],['fsvsdv', 'zxce', 'D12fv']]
        correctList = [[' Assignment 2', ' TDT4300 DATAVAREH/DATAGRUVED', '2017-03-10', '08:00:00'], [' Assignment 2:', ' TDT4140 PROGRAMVAREUTVIKL', '2017-03-10', '23:55:00'],['', '', '00-00-00', '00:00:00']]
        self.assertEqual(prepAllDeiveriesForDatabase(scrapeList),correctList)
    # def test_getUsername(self):
    #     correctUname="eirikriv"
    #     username = getUsername()
    #     self.assertEqual(username,correctUname)
    # def test_getUsername(self):
    #     correctPass="12345"
    #     password = getUserPassword()
    #     self.assertEqual(password,correctPass)
    def test_convertweekAndDayToDate_sample_dates_correct(self):
        days = ["Mandag","Tirsdag","Onsdag","Torsdag","Fredag"]
        weeks = ["01","20","51","50","24"]
        year = ["2012","2016","2016","2017","2018"]
        correctOutput = ["2012-01-02","2016-05-17", "2016-12-21","2017-12-14","2018-06-15"]
        for n in range(len(days)):
            self.assertEqual(convertweekAndDayToDate(days[n],weeks[n],year[n]), correctOutput[n])
    
    def test_readCourseFileReturnAllLectureExersiseEvents_sample_scrapes_correct(self):
        testInput=['Mandag 08:15 - 10:00 2-14,17 \xc3\x98ving BIT, MLREAL, MTDT, MTING, MTI\xc3\x98T, MTTK R1', 'Tirsdag 16:15 - 18:00 2-14,17 Forelesning BIT, MLREAL, MTDT, MTING, MTI\xc3\x98T, MTTK R1', 'Fredag 14:15 - 16:00 2-14,16 Forelesning BIT, MLREAL, MTDT, MTING, MTI\xc3\x98T, MTTK R1']
        correctOutput = ['2017-01-09T08:15:00', '2017-01-09T10:00:00', '\xc3\x98ving', 'R1']
        self.assertEqual(readCourseFileReturnAllLectureExersiseEvents(testInput,"2017"),correctOutput)

    #def test_scrapeNtnuCourseWebsites_correct(self):
     #   correctOutput=['Mandag 08:15 - 10:00 2-14,17 \xc3\x98ving BIT, MLREAL, MTDT, MTING, MTI\xc3\x98T, MTTK R1', 'Tirsdag 16:15 - 18:00 2-14,17 Forelesning BIT, MLREAL, MTDT, MTING, MTI\xc3\x98T, MTTK R1', 'Fredag 14:15 - 16:00 2-14,16 Forelesning BIT, MLREAL, MTDT, MTING, MTI\xc3\x98T, MTTK R1']
      #  self.assertEqual(scrapeNtnuCourseWebsites("TDT4140"),correctOutput)
    
    #def test_scrapeNtnuCourseWebsites_incorrect(self):
     #   
      #  self.assertEqual(scrapeNtnuCourseWebsites("TD4140"),"")
    # def test_insertUserIntoDatabase_correctInsert(self):
    #     userName="Eirik Rivedal"
    #     userID= "1400"
    #     insertUserIntoDatabase(userID,userName)
    #     self.assertEqual(getEntryFromUserTable(userID),(userID, userName))

    # def test_insertCourseIntoDatabase_correctInsert(self):
    #     courseID="0011"
    #     courseName= "TDT4140"
    #     insertCourseIntoDatabase(courseID,courseName)
    #     self.assertEqual(getEntryFromCourseTable(courseID),(courseID, courseName))
    
    # def test_insertAssignmentIntoDatabase_correctInsert(self):
    #     assignmentID="0008"
    #     assignmnentDate= "2017-12-20"
    #     assignmnentTime= "23:59:00"
    #     insertAssignmnentIntoDatabase(assignmentID,assignmnentDate,assignmnentTime)
    #     self.assertEqual(getEntryFromAssignmnentTable(assignmentID),(assignmentID, assignmnentDate,assignmnentTime))
    
    # def test_insertLectureIntoDatabase_correctInsert(self):
    #     lectureID="0008"
    #     lectureDate= "2017-12-20"
    #     lectureStartTime= "08:15:00"
    #     lectureEndTime ="10:00:00"
    #     lectureDescription="Lecture in TDT 4140"
    #     lectureLocation="R1"
    #     insertLectureIntoDatabase(lectureID,lectureDate,lectureStartTime,lectureEndTime,lectureDescription,lectureLocation)
    #     self.assertEqual(getEntryFromLectureTable(lectureID),(lectureID, lectureDate, lectureDescription, lectureLocation, lectureStartTime,lectureEndTime))
    
        





if __name__ == '__main__':
    unittest.main()