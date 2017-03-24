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
import time
def controllScannForLecturesandInsert(courseCode):
	lectures , courseCode = scrapeNtnuCourseWebsites("TDT4140")
	lectureTimes = readCourseReturnAllLectureExersiseEvents(lectures, courseCode, "2017")
	counter = 0
	errorCounter = 0
	engine = create_engine(URI)
	connection = engine.connect()
	if(not getValueFromCourseTable(engine, connection, courseCode)):
		insertCourseIntoDatabase(engine, connection,courseCode, courseCode)
	for types in lectureTimes:
		for events in types:
			try:
				lastEntry = getLastEntryFromLectureTable(engine, connection)
				lectureID = lastEntry[0]
				lectureID = str(int(lectureID)+1)
				lectureID = (6-len(lectureID))*"0" + lectureID
			except:
				lectureID = "000001"
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
	print "successfully inserted: " + str(counter) + " of: " + str(errorCounter+counter) +  " entries" 
#controllScannForLecturesandInsert("TDT4140")

def controllScannForAssignmentsAndInsert():
	formScrape = prepAllDeiveriesForDatabase(loginAndGetAllCurrentAssignements(6))
	engine = create_engine(URI)
	connection = engine.connect()
	counter = 0
	errorCounter = 0
	for assigment in fromScrape:
		courseCode = assigment[1].split()[0]
		if(getValueFromCourseTable(engine, connection, courseCode)):
			insertCourseIntoDatabase(courseCode, courseCode)
		try:
			lastEntry = getLastEntryFromAssignmentTable(engine, connection)
			assigmentID = lastEntry[0]
			assigmentID = str(int(assigmentID)+1)
			assigmentID = (6-len(assigmentID))*"0" + assigmentID
		except:
			assigmentID = "000001"
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
	print "successfully inserted: " + str(counter) + " of: " + str(errorCounter+counter) +  " entries" 
#controllScannForAssignmentsAndInsert()	


def getLecturesAndInsertIntoCalendar(stringStudentId):
	engine = create_engine(URI)
	connection = engine.connect()
	courseIDs = getEntriesFromStudent_courseTable(engine, connection,stringStudentId)
	eventColor = "3"
  	for entries in courseIDs:
  		lectureID = getLectureIDsFromLecture_courseTable(engine,connection,entries[1])
  		for lec in lectureID:
  			lectureDetails = getEntriesFromLectureTable(engine, connection,lec[0])
  			print lectureDetails[0][1]
  			tittel = lectureDetails[0][2]
  			startdato = lectureDetails[0][1]
  			sluttdato = lectureDetails[0][1]
  			starttid = lectureDetails[0][4]
  			sluttid = lectureDetails[0][5]
  			beskrivelse = lectureDetails[0][2]
  			sted = lectureDetails[0][3]
  			insertEventToCal(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,eventColor)
  			time.sleep(2)
#getLecturesAndInsertIntoCalendar("000001")

def getassignmentDeadLineAndInsertIntoDatabase(stringStudentID):
	engine = create_engine(URI)
	connection = engine.connect()
	eventColor = "4"
	eventColorForWordSessions = "11"
	assignmentDetailList = []
	assignmentIDs = getEntriesFromAssignmentStudentAllAssforStud(engine, connection,stringStudentID)
	for entries in assignmentIDs:
		tempList = []
		assignmentDetails = getEntryFromAssigmnentTable(engine, connection,entries[1])
		assignmentDetailList.append(assignmentDetails)
		tittel = assignmentDetails[3]
  		startdato = assignmentDetails[1]
  		sluttdato = assignmentDetails[1]
  		starttid = assignmentDetails[2]
  		sluttid = str(assignmentDetails[2])[0:3] + "05:00"
  		beskrivelse = assignmentDetails[3]
  		sted = " "	
  		insertEventToCal(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,eventColor)
  		time.sleep(4)

  	for dl in assignmentDetailList:
  		eventsPriorToDeadline = getEventsDaysBack(dl[1],dl[2],3)
  		studentInitialHours = int(getEntryFromAssignmentStudentInitialHoursForStudent(engine,connection,dl[0])[0][2])
  		deadline = dl[1] + " " + dl[2]
  		plannedEvents = OwlbrainScheduler(deadline,studentInitialHours,eventsPriorToDeadline,6)
  		for suggestions in plannedEvents:
			tittel = dl[3]
  			startdato = suggestions[2]
  			sluttdato = suggestions[2]
  			starttid = suggestions[0]
  			sluttid = suggestions[1]
  			beskrivelse = dl[3]
  			sted = "Your favorite studyplace"
  			insertEventToCal(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,eventColorForWordSessions)
  		time.sleep(4)
def main(stringStudentID):
	getLecturesAndInsertIntoCalendar(stringStudentID)
	time.sleep(4)
	getassignmentDeadLineAndInsertIntoDatabase(stringStudentID)
main("000001")


