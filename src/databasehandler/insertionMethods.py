from sqlalchemy import create_engine, MetaData, Table, select
from connectHerokuMYSQL import *
import traceback

def removeAtgmailcomFromString(gmail):
	if(gmail.find("@")):
		return gmail.split("@")[0]
	else:
		return gmail

def insertNewStudentIntoDatabase(stringUniqueGmail,stringStudentName):
	returnValue =False
	gmailWithoutLastPart = removeAtgmailcomFromString(stringUniqueGmail)
	try:
		insertStudentIntoDatabase(gmailWithoutLastPart,stringStudentName)
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

def insertLectureIntoDatabase(engine, connection, stringLectureID,stringLectureDate,stringLectureStartTime,stringLectureEndTime,stringDescription,stringWhere):
	returnValue = False
	try:
		insertLecturesIntoDatabase(engine, connection, stringLectureID,stringLectureDate,stringLectureStartTime,stringLectureEndTime,stringDescription,stringWhere)
		returnValue=True
	except:	
		print traceback.print_exc()
	return returnValue

def insertStudentCourseIntoDatabase(stringUniqueGmail,course): #Requires a pure list of courses atm
	returnValue = False
	try:
		insertStudent_courseIntoDatabase(stringUniqueGmail,course)
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
		getEntriesFromCourseTable(engine, connection, stringCourseID)
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



