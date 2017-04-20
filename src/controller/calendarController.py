import sys
sys.path.append("../scraper")
sys.path.append("../scheduler")
sys.path.append("../owlbrain")
sys.path.append("../databasehandler")
from owlbrain import *
from calendarMethods import *
from insertionMethods import *
import traceback
from databaseConnectDetails import *
from schedulerHelperMethods import *
from datetime import datetime
from datetime import date
import datetime as dt
import time

def updateStudentAssignments(stringStudentID):
    engine = create_engine(URI)
    connection = engine.connect()
    temp = getEntriesFromStudent_courseTable(engine, connection,stringStudentID)
    for n in temp:
        ass_course = getEntriesFromAssignment_courseTableReturnAssignments(engine,connection,n[1])
        if(ass_course!=[]):
            for assignmentID in ass_course:
                assignmentID = assignmentID[0]
                try:
                    insertStudent_Assignment(engine,connection,stringStudentID,assignmentID)
                except: 
                    None


def getLecturesAndInsertIntoCalendar(stringStudentId):
    engine = create_engine(URI)
    connection = engine.connect()
    refreshToken = getUserReffreshToken(engine, connection, stringStudentId)
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
    if(success):
        updateDBWithCurrentCalUpdate(engine,connection,stringStudentId)
    return success
#getLecturesAndInsertIntoCalendar("100867243925223857971")

def useHubroToFindTimeSlotsForAssignments(assignmentDetails,studentID,refreshToken):
    engine = create_engine(URI)
    connection = engine.connect()
    eventColorForWordSessions = "6"
    success = False
    daysBack = findDaysBetweenDates(assignmentDetails[1])
    print daysBack
    refreshToken = refreshToken
    dl = assignmentDetails
    if(True):
        courseID = getEntryFromAssignment_courseTable(engine,connection,dl[0])[1]
        eventsPriorToDeadline = getEventsDaysBack(dl[1],dl[2],daysBack,refreshToken)
        studentInitialHours = int(str(getAvgHoursForStudentInCourse(engine, connection,studentID,courseID).hour))
        if(eventsPriorToDeadline and studentInitialHours == None):
            return success
        else:
            deadline = dl[1] + " " + dl[2]
            print eventsPriorToDeadline
            plannedEvents = OwlbrainScheduler(deadline,studentInitialHours,eventsPriorToDeadline,daysBack+2)
            print plannedEvents
            for suggestions in plannedEvents:
                title = dl[3]
                startDate = suggestions[2]
                endDate = suggestions[2]
                startTime = suggestions[0]
                endTime = suggestions[1]
                description = "Work on assignment"
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
        updateStudentAssignments(stringStudentID)
        assignmentIDs = getEntriesFromAssignmentStudentAllAssforStud(engine,connection,stringStudentID)
    except:
        assignmentIDs=None
    if(assignmentIDs==None):
        return success
    else:
        for entries in assignmentIDs:
            print entries
            tempList = []
            assignmentDetails = getEntryFromAssigmnentTable(engine,connection,entries[1])[0]
            assignmentDetailList.append(assignmentDetails)
            title = assignmentDetails[3]
            startDate = assignmentDetails[1]
            endDate = assignmentDetails[1]
            startTime = assignmentDetails[2]
            endTime = str(assignmentDetails[2])[0:5] + ":59"
            description = assignmentDetails[3]
            location = " "    
            insertEventToCal(title,startDate,endDate,startTime,endTime,description,location,eventColor,refreshToken)
            useHubroToFindTimeSlotsForAssignments(assignmentDetails,stringStudentID,refreshToken)
            success = True
    if(success):
        updateDBWithCurrentCalUpdate(engine,connection,stringStudentID)
    return success 
#getassignmentDeadLineAndInsertIntoCalendar("100867243925223857971")
#test for studentID = 100867243925223857971

def checkStudentSettingsAndInsertLecAndOrAssignments(stringStudentID):
    engine = create_engine(URI)
    connection = engine.connect()
    studentEntry = getStudent_settingFromStudentTable(stringStudentID)
    if(studentEntry[2]=="1"):
        getassignmentDeadLineAndInsertIntoCalendar(stringStudentID)
    elif(studentEntry[3]=="1"):
        getLecturesAndInsertIntoCalendar(stringStudentID)
    else:
        print "User does not want hubro to update schedual for assignments and lectures"


