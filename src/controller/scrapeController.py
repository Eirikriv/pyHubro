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
	year = now.year
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
				if(findDaysBetweenDates(date)==0):
					None
				else:
					try:
						insertLectureIntoDatabase(engine,connection,lectureID,date,start,end,description,where)
						insertLectureCourseIntoDatabase(engine,connection,lectureID,courseCode)
					except:
						None
scanForLecturesInCourseAndInsert("TDT4140","2017")

def scanForAssignmentInACourseAndInsert(courseCodeToScanFor):
	try:
		formScrape = prepAllDeiveriesForDatabase(loginAndGetAllCurrentAssignements(6))
		engine = create_engine(URI)
		connection = engine.connect()
	except:
		return None
	counter = 0
	errorCounter = 0
	for assigment in fromScrape:
		courseCode = assigment[1].split()[0]
		if(courseCode==courseCodeToScanFor):
			assignmentID = assigment[1].split()[0]+assigment[2]+assigment[3]
			if(checkIfAssignmentIsInAssignmentTable(engine,connection,assignmentID)):
				print "Assignment already in table"
			else:
				stringAssignmentDate = assigment[2]
				stringAssignmentTime = assigment[3]
				stringAssignmentDescription = assigment[0]
				infoString = assigment[1].split()
				for n in range(1,len(infoString)):
					stringAssignmentDescription = stringAssignmentDescription + " " + infoString[n]
				if(insertAnAssignmentIntoDatabase(engine, connection ,assigmentID,stringAssignmentDate,stringAssignmentTime,stringAssignmentDescription)):
					insertAssignment_courseIntoDatabase(engine, connection, assigmentID, courseCode)
					counter += 1
				else:
					errorCounter += 1 
	return counter, errorCounter

#scanForAssignmentInACourseAndInsert

