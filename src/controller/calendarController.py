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

def updateStudentAssignments(engine, connection, stringStudentID): #Helperfunction, updates the table "studentAssignment" 
    engine = engine                                                #Nessessary for the system to link a student to an assignment
    connection = connection
    temp = getEntriesFromStudent_courseTable(engine, connection,stringStudentID)
    for n in temp:
        ass_course = getEntriesFromAssignment_courseTableReturnAssignments(engine,connection,n[1])
        if(ass_course!=[]):
            for assignmentID in ass_course:
                assignmentID = assignmentID[0]
                insertStudent_Assignment(engine,connection,stringStudentID,assignmentID)


def getLecturesAndInsertIntoCalendar(engine, connection, stringStudentId): #Updates the google calendar for a student
    engine = engine                                                        # with lectures he or she registered for
    connection = connection
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
                        if(findDaysBetweenDates(startdate)==0):
                            None
                        else:
                            try:
                                insertEventToCal(title,startdate,endDate,startTime,endTime,description,location,eventColor,refreshToken)
                                success = True
                            except:
                                None
    if(success):
        updateDBWithCurrentCalUpdate(engine,connection,stringStudentId)
    return success

def useHubroToFindTimeSlotsForAssignments(assignmentDetails,studentID,refreshToken): #Helperfunction, the alorithm used
    engine = create_engine(URI)                                                      #to find awalible spots in a students
    connection = engine.connect()                                                    #calendar
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



def getassignmentDeadLineAndInsertIntoCalendar(engine, connection, stringStudentID): #Updates the students calendar with 
    engine = engine                                                                  #assignments he or she registered for
    connection = connection
    refreshToken = getUserReffreshToken(engine, connection,stringStudentID)
    eventColor = "4"
    assignmentDetailList = []
    success = False
    try:
        updateStudentAssignments(engine, connection,stringStudentID)
    except:
        None
    assignmentIDs = getEntriesFromAssignmentStudentAllAssforStud(engine,connection,stringStudentID)
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


def checkStudentSettingsAndInsertLecAndOrAssignments(stringStudentID):  #Main method, when a certain URL request is sent to
    engine = create_engine(URI)                                         #www.eirikriv.pythonanywhere.com, this function runs
    connection = engine.connect()                                       #Either updates calendar with lectures, assignments or 
    studentEntry = getStudent_settingFromStudentTable(engine, connection,stringStudentID) # none
    print(studentEntry)
    if(str(studentEntry[0][2])=="1"):
        getassignmentDeadLineAndInsertIntoCalendar(engine, connection, stringStudentID)
    elif(str(studentEntry[0][3])=="1"):
        getLecturesAndInsertIntoCalendar(engine, connection, stringStudentID)
    else:
        print "User does not want hubro to update schedual for assignments and lectures"


