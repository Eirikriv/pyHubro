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

def scanForLecturesInCourseAndInsert(courseCode, year, if_spring_set_0_if_fall_set_1_str):
	counter = 0
	errorCounter = 0
	try:
		engine = create_engine(URI)
		connection = engine.connect()
	except:
		engine = None
		connection = None
	try:
		lectures , courseCode = scrapeNtnuCourseWebsites(courseCode)
		lectureTimes = readCourseReturnAllLectureExersiseEvents(lectures, courseCode, year)
	except:
		lectures = None
		lectureTimes = None
	if(courseCode!=None):
		uniqueLectureString = courseCode+year+if_spring_set_0_if_fall_set_1_str+"000"
	else:
		uniqueLectureString = None
	if(getALectureFromLectureTable(engine, connection,uniqueLectureString)):
		print("Lectures for that course is already in database")
	elif(lectures and lectureTimes != None):
		if(not getValueFromCourseTable(engine, connection, courseCode)):
			insertCourseIntoDatabase(engine, connection,courseCode, courseCode)
		for types in lectureTimes:
			for events in types:
				try: #"TDT41400000"
					lastEntry = getLastEntryFromLectureTable(engine, connection)
					lectureID = lastEntry[0]
					temp = lectureID[9:12]
					newLectureID = str(int(temp)+1)
					temp2 = lectureID[0:9] 
					if(len(newLectureID)==1):
						lectureID=temp2+"00"+newLectureID
					elif(len(newLectureID)==2):
						lectureID=temp2+"0"+newLectureID
					else:
						lectureID = temp2+newLectureID
				except:
					lectureID = uniqueLectureString
				date = events[1].split("T")[0]
				start = events[1].split("T")[1]
				end = events[2].split("T")[1]
				description = events[3]
				where=events[4]
				if(insertLectureIntoDatabase(engine,connection,lectureID,date,start,end,description,where)):
					counter += 1
					insertLectureCourseIntoDatabase(engine,connection,lectureID,courseCode)
				else:
					errorCounter += 1 
	return (counter, errorCounter, lectures)
scanForLecturesInCourseAndInsert("TDT4140", "2017" , "0")
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

