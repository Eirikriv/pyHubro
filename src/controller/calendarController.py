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
  eventColor = "3"
  success = False
  try:
    courseIDs = getEntriesFromStudent_courseTable(engine, connection,stringStudentId)
	except:
    courseIDs = None
  if(courseIDs==None):
    print("No courses found")
    return success
  else:
    for entries in courseIDs:
      try:
        lectureID = getLectureIDsFromLecture_courseTable(engine,connection,entries[1])
      except:
        lectureID=None
      if(lectureID==None):
        print("No lectures found for this course")
        return success
      else:
        for lec in lectureID:
          try:
            lectureDetails = getEntriesFromLectureTable(engine, connection,lec[0])
          except:
            lectureDetails=None
          if(lectureDetails==None):
            print("No lectures found")
            return success
          else:
            title = lectureDetails[0][2]
            startDate = lectureDetails[0][1]
  			    endDate = lectureDetails[0][1]
            startTime = lectureDetails[0][4]
  			    endTime = lectureDetails[0][5]
  			    description = lectureDetails[0][2]
  			    location = lectureDetails[0][3]
            try:
              insertEventToCal(title,startdate,endDate,startTime,endTime,description,location,eventColor)
              success = True
            except:
              None
    return success
#getLecturesAndInsertIntoCalendar("000001")

def getassignmentDeadLineAndInsertIntoCalendar(stringStudentID):
	engine = create_engine(URI)
	connection = engine.connect()
	eventColor = "4"
	assignmentDetailList = []
  success = False
  try:
    assignmentIDs = getEntriesFromAssignmentStudentAllAssforStud(engine, connection,stringStudentID)
  except:
    assignmentIDs=None
  if(assignmentIDs==None):
    return success
  else:
    for entries in assignmentIDs:
      tempList = []
      assignmentDetails = getEntryFromAssigmnentTable(engine, connection,entries[1])
		  assignmentDetailList.append(assignmentDetails)
		  tittel = assignmentDetails[3]
  		startdato = assignmentDetails[1]
  		sluttdato = assignmentDetails[1]
  		starttid = assignmentDetails[2]
  		sluttid = str(assignmentDetails[2])[0:5] + ":59"
  		beskrivelse = assignmentDetails[3]
  		sted = " "	
  		try:
        insertEventToCal(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,eventColor)
        success = True
      except:
        None
    useHubroToFindTimeSlotsForAssignments(assignmentDetails)
    return success 


def useHubroToFindTimeSlotsForAssignments(assignmentDetails,daysBack):
  eventColorForWordSessions = "6"
  success = False
  for dl in assignmentDetailList:
    try:
      eventsPriorToDeadline = getEventsDaysBack(dl[1],dl[2],daysBack)
  	  studentInitialHours = int(getEntryFromAssignmentStudentInitialHoursForStudent(engine,connection,dl[0])[0][2])
    except:
      eventsPriorToDeadline = None
      studentInitialHours = None
    if(eventsPriorToDeadline or studentInitialHours == None):
      return success
    else:
      deadline = dl[1] + " " + dl[2]
      plannedEvents = OwlbrainScheduler(deadline,studentInitialHours,eventsPriorToDeadline,daysBack+2)
      for suggestions in plannedEvents:
        title = dl[3]
        startDate = suggestions[2]
        endDate = suggestions[2]
        startTime = suggestions[0]
        endTime = suggestions[1]
        description = dl[3]
        location = "Your favorite workplace"
  		  insertEventToCal(title,startDate,endDate,startTime,endTime,description,location,eventColorForWordSessions)
        success = True
      return success
      
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
