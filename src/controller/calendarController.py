import sys
sys.path.append("../scraper")
sys.path.append("../scheduler")
sys.path.append("../owlbrain")
sys.path.append("../databasehandler")

from owlbrainV1 import *
from calendarMethods import *
from insertionMethods import *
from scrapeForCourseLectureTimes import *
import traceback
from databaseConnectDetails import *
from scrapeItslearningForAssignements import *
import time

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
	eventColorForWordSessions = "6"
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
  		print eventsPriorToDeadline
  		studentInitialHours = int(getEntryFromAssignmentStudentInitialHoursForStudent(engine,connection,dl[0])[0][2])
  		deadline = dl[1] + " " + dl[2]
  		print deadline
  		print studentInitialHours
  		plannedEvents = OwlbrainScheduler(deadline,studentInitialHours,eventsPriorToDeadline,5)
  		for suggestions in plannedEvents:
			print suggestions
			tittel = dl[3]
  			startdato = suggestions[2]
  			sluttdato = suggestions[2]
  			starttid = suggestions[0]
  			sluttid = suggestions[1]
  			beskrivelse = dl[3]
  			sted = "Your favorite studyplace"
  			insertEventToCal(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,eventColorForWordSessions)
  		time.sleep(4)

def insertOnlyPlannedEvents(stringStudentID):
	engine = create_engine(URI)
	connection = engine.connect()
	eventColor = "4"
	eventColorForWordSessions = "6"
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
  		#insertEventToCal(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,eventColor)
  		#time.sleep(4)

  	for dl in assignmentDetailList:
  		eventsPriorToDeadline = getEventsDaysBack(dl[1],dl[2],3)
  		print eventsPriorToDeadline
  		studentInitialHours = int(getEntryFromAssignmentStudentInitialHoursForStudent(engine,connection,dl[0])[0][2])
  		deadline = dl[1] + " " + dl[2]
  		print deadline
  		print studentInitialHours
  		plannedEvents = OwlbrainScheduler(deadline,studentInitialHours,eventsPriorToDeadline,5)
  		print plannedEvents
  		for suggestions in plannedEvents:
			print suggestions
			tittel = dl[3]
  			startdato = suggestions[2]
  			sluttdato = suggestions[2]
  			starttid = suggestions[0]
  			sluttid = suggestions[1]
  			beskrivelse = dl[3]
  			sted = "Your favorite studyplace"
  			insertEventToCal(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,eventColorForWordSessions)
  		time.sleep(4)
