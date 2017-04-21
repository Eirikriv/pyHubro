import sys
sys.path.append("../scraper")
sys.path.append("../scheduler")
sys.path.append("../owlbrain")
from owlbrainV1 import *
from calendarMethods import *
from insertionMethods import *
from scrapeForCourseLectureTimes import *
import traceback
from databaseConnectDetails import *
from scrapeItslearningForAssignements import *
from databaseUtils import *
import time
import datetime

def scanForLecturesInCourseAndInsert(courseCode):
	counter = 0
	errorCounter = 0
	engine = create_engine(URI)
	connection = engine.connect()
	now = datetime.datetime.now()
	year = str(now.year)
	lectures , courseCode = scrapeNtnuCourseWebsites(courseCode)
	lectureTimes = readCourseReturnAllLectureExersiseEvents(lectures, courseCode, year)
	print lectureTimes
	print lectures
	print courseCode
	if(True):
		for types in lectureTimes:
			for events in types:
				date = events[1].split("T")[0]
				start = events[1].split("T")[1]
				end = events[2].split("T")[1]
				description = events[3]
				where=events[4]
				lectureID = courseCode+date+"T"+start
				try:
					if(insertLectureIntoDatabase(engine,connection,lectureID,date,start,end,description,where)):
						insertLectureCourseIntoDatabase(engine,connection,lectureID,courseCode)
				except:
					None
#scanForLecturesInCourseAndInsert("TDT4140")

def scanForAssignmentInACourseAndInsert():
	#fromScrape = prepAllDeiveriesForDatabase(loginAndGetAllCurrentAssignements(3))
	fromSrape = [[u' Assignment 5', u' TDT4300 DATAVAREH/DATAGRUVED', u'2017-04-21', u'23:55:00'], [u' Assignment 2.2', u' TI\xd84317 EMPIRISK FINANS', u'2017-04-21', u'23:59:00'], [u' Step 7:', u' TDT4140 PROGRAMVAREUTVIKL', u'2017-04-27', u'12:00:00'], [u' Assignment 10', u' TI\xd84140 PROSJEKTFINANS', u'2017-05-01', u'23:59:00'], [u' Assignment 2.3', u' TI\xd84317 EMPIRISK FINANS', u'2017-05-05', u'23:59:00']]
	engine = create_engine(URI)
	connection = engine.connect()
	print fromScrape
	for assigment in fromScrape:
		courseCode = assigment[1].split()[0]
		assignmentID = courseCode+assigment[2]+assigment[3]
		if(checkIfAssignmentIsInAssignmentTable(engine,connection,assignmentID)):
			print "Assignment already in table"
		else:
			stringAssignmentDate = assigment[2]
			stringAssignmentTime = assigment[3]
			stringAssignmentDescription = assigment[0] + "in" + assigment[1]
			infoString = assigment[1].split()
			for n in range(1,len(infoString)):
				stringAssignmentDescription = stringAssignmentDescription + " " + infoString[n]
			if(insertAnAssignmentIntoDatabase(engine, connection ,assigmentID,stringAssignmentDate,stringAssignmentTime,stringAssignmentDescription)):
				insertAssignment_courseIntoDatabase(engine, connection, assigmentID, courseCode)
scanForAssignmentInACourseAndInsert()

def automaticScrape():
	engine = create_engine(URI)
	connection = engine.connect()
	courseCodes = getAllCourseCodes(engine,connection)
	for courseCode in courseCodes:
		scanForLecturesInCourseAndInsert(courseCode)
	scanForAssignmentInACourseAndInsert()

