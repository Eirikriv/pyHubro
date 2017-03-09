from sqlalchemy import create_engine, MetaData, Table, select
from connectHerokuMYSQL import *
import traceback

def removeAtgmailcomFromString(gmail):
	if(gmail.find("@")):
		return gmail.split("@")[0]
	else:
		return gmail

def insertNewUserIntoDatabase(stringUniqueGmail,stringUserName):
	returnValue =False
	gmailWithoutLastPart = removeAtgmailcomFromString(stringUniqueGmail)
	try:
		insertUserIntoDatabase(gmailWithoutLastPart,stringUserName)
		returnValue = True
	except:
		print traceback.print_exc()
	return returnValue

def insertCourseIntoDatabase(stringCourseID,stringCourseName):
	returnValue =False
	try:
		insertACourseIntoDatabase(stringCourseID,stringCourseName)
		returnValue = True
	except:
		print traceback.print_exc()
	return returnValue

def insertAnAssignmentIntoDatabase(stringAssignmnentID,stringAssignmnentDate,stringAssignmnentTime):
	returnValue =False
	try:
		insertAssignmnentIntoDatabase(stringAssignmnentID,stringAssignmnentDate,stringAssignmnentTime)
		returnValue=True
	except:
		print traceback.print_exc()
	return returnValue

def insertLectureIntoDatabase(engine, connection, stringLectureID,stringLectureDate,stringLectureStartTime,stringLectureEndTime,stringDescription,stringWhere):
	returnValue = False
	try:
		insertLecturesIntoDatabase(engine, connection, stringLectureID,stringLectureDate,stringLectureStartTime,stringLectureEndTime,stringDescription,stringWhere)
		returnValue=True
	except:	
		print traceback.print_exc()
	return returnValue

def insertUserCourseIntoDatabase(stringUniqueGmail,course): #Requires a pure list of courses atm
	returnValue = False
	try:
		insertUser_courseIntoDatabase(stringUniqueGmail,course)
		returnValue=True
	except:
		print traceback.print_exc()
	return returnValue
		
def insertLectureCourseIntoDatabase(engine, connection, stringLectureID,stringCourseID):
	returnValue =False
	try:
		insertLecture_courseIntoDatabase(engine,connection,stringLectureID,stringCourseID)
		returnValue = True
	except:
		print traceback.print_exc()
	return returnValue

def getValueFromCourseTable(engine, connection, stringCourseID):
	returnValue = False
	try:
		getEntryFromCourseTable(engine, connection, stringCourseID)
		returnValue = True
	except:
		print traceback.print_exc()
	return returnValue

def insertAnAssignmentIntoDatabase(engine, connection ,stringAssignmnentID,stringAssignmentDate,stringAssignmentTime,stringAssignmentDescription):
	returnValue = False
	try:
		insertAssignmentIntoDatabase(engine, connection, stringAssignmnentID,stringAssignmentDate,stringAssignmentTime,stringAssignmentDescription)
		returnValue = True
	except:
		print traceback.print_exc()
	return returnValue



