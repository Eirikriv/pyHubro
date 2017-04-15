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
  refreshToken = getUserReffreshToken(engine, connection, stringStudentID)
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
              insertEventToCal(title,startdate,endDate,startTime,endTime,description,location,eventColor,refreshToken)
              success = True
            except:
              None
    return success
#getLecturesAndInsertIntoCalendar("000001")

def useHubroToFindTimeSlotsForAssignments(assignmentDetails,daysBack,refreshToken):
  engine = create_engine(URI)
  connection = engine.connect()
  eventColorForWordSessions = "6"
  success = False
  refreshToken = 
  for dl in assignmentDetailList:
    try:
      eventsPriorToDeadline = getEventsDaysBack(dl[1],dl[2],daysBack,refreshToken)
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
        insertEventToCal(title,startDate,endDate,startTime,endTime,description,location,eventColorForWordSessions,refreshToken)
        success = True
      return success

def getassignmentDeadLineAndInsertIntoCalendar(stringStudentID):
	engine = create_engine(URI)
	connection = engine.connect()
  refreshToken = getUserReffreshToken(engine, connection,stringStudentID)
	eventColor = "4"
	assignmentDetailList = []
  success = False
  try:
    assignmentIDs = getEntriesFromAssignmentStudentAllAssforStud(engine,connection,stringStudentID)
  except:
    assignmentIDs=None
  if(assignmentIDs==None):
    return success
  else:
    for entries in assignmentIDs:
      tempList = []
      assignmentDetails = getEntryFromAssigmnentTable(engine,connection,entries[1])
		  assignmentDetailList.append(assignmentDetails)
		  tittel = assignmentDetails[3]
  		startdato = assignmentDetails[1]
  		sluttdato = assignmentDetails[1]
  		starttid = assignmentDetails[2]
  		sluttid = str(assignmentDetails[2])[0:5] + ":59"
  		beskrivelse = assignmentDetails[3]
  		sted = " "	
  		try:
        insertEventToCal(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,eventColor,refreshToken)
        success = True
      except:
        None
    useHubroToFindTimeSlotsForAssignments(assignmentDetails,refreshToken)
    return success 
#test for studentID = 100867243925223857971
def checkStudentSettingsAndInsertLecAndOrAssignments(stringStudentID):
  engine = create_engine(URI)
  connection = engine.connect()
  studentEntry = getStudent_settingFromStudentTable(stringStudentID)
  if(studentEntry[2]=="1"):
    getassignmentDeadLineAndInsertIntoCalendar(stringStudentID)
  elif(studentEntry[3]=="1"):
    useHubroToFindTimeSlotsForAssignments(stringStudentID)
  else:
    print "User does not want hubro to update schedual for assignments and lectures"


