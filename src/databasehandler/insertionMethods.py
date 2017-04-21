from sqlalchemy import create_engine, MetaData, Table, select
from databaseUtils import *
import traceback

def updateDBWithCurrentCalUpdate(engine, connection,stringStudentId):
	returnValue =False
	try:
		dtDateToUpload = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
		engine = engine
		connection = connection
		metadata = MetaData()
		student = Table('student', metadata, autoload=True , autoload_with=engine)
		update = student.update(student).where(student.c.studentID==stringStudentId).values(updatedCalendars=dtDateToUpload)
		connection.execute(update)
		returnValue = True
	except:
		print traceback.print_exc()
	return returnValue

def insertCourseIntoDatabase(engine, connection,stringCourseID,stringCourseName):
	returnValue =False
	try:
		engine = engine
		connection = connection
		metadata = MetaData()
		course = Table('course', metadata, autoload=True , autoload_with=engine)
		ins = course.insert()
		new_course = ins.values(courseID=stringCourseID,courseName=stringCourseName)
		connection.execute(new_course)
		returnValue = True
	except:
		print traceback.print_exc()
	return returnValue

def insertLectureIntoDatabase(engine, connection, stringLectureID,stringLectureDate,stringLectureStartTime,stringLectureEndTime,stringDescription,stringWhere):
	returnValue = False
	try:
		engine = engine
		connection = connection
		metadata = MetaData()
		lecture = Table('lecture', metadata, autoload=True , autoload_with=engine)
		ins = lecture.insert()
		new_lecture = ins.values(lectureID=stringLectureID,lectureDate=stringLectureDate,lectureStartTime=stringLectureStartTime,lectureEndTime=stringLectureEndTime,lectureDescription=stringDescription,lectureLocation=stringWhere)
		connection.execute(new_lecture)
		returnValue = True
	except:	
		print traceback.print_exc()
	return returnValue

		
def insertLectureCourseIntoDatabase(engine, connection, stringLectureID,stringCourseID):
	returnValue =False
	try:
		engine = engine
		connection = connection
		metadata = MetaData()
		lecture_course = Table('lecture_course', metadata, autoload=True , autoload_with=engine)
		ins = lecture_course.insert()
		new_lecture_course = ins.values(lectureID=stringLectureID,courseID=stringCourseID)
		connection.execute(new_lecture_course)
		returnValue = True
	except:
		print traceback.print_exc()
	return returnValue

def getValueFromCourseTable(engine, connection, stringCourseID):
	returnValue = False
	try:
		engine = engine
		connection = connection
		metadata = MetaData()
		course = Table('course', metadata, autoload=True , autoload_with=engine)
		selectCourse = select([course]).where(course.c.courseID == stringCourseId)
		returnValue = list(connection.execute(selectCourse))
	except:
		print traceback.print_exc()
	return returnValue

def insertAnAssignmentIntoDatabase(engine, connection ,stringAssigmentID,stringAssignmentDate,stringAssignmentTime,stringAssignmentDescription):
	returnValue = False
	engine = engine
	connection = connection
	metadata = MetaData()
	assignmnent = Table('assignment', metadata, autoload=True , autoload_with=engine)
	ins = assignmnent.insert()
	new_assignmnent = ins.values(assignmentID=stringAssigmentID,assignmentDate=stringAssignmentDate,assignmentTime=stringAssignmentTime,assignmentDescription=stringAssignmentDescription)
	connection.execute(new_assignmnent)
	returnValue = True
	print traceback.print_exc()
	return returnValue

def getALectureFromLectureTable(engine, connection,stringLectureID):
	returnValue = False
	try:
		engine = engine
		connection = connection
		metadata = MetaData()
		lecture = Table('lecture', metadata, autoload=True , autoload_with=engine)
		selectLecture = select([lecture]).where(lecture.c.lectureID == stringLectureID)
		returnValue = connection.execute(selectLecture)
		returnValue = True
	except:
		print traceback.print_exc()
	return returnValue

def checkIfAssignmentIsInAssignmentTable(engine,connection,stringAssignmentID):
	returnValue = False
	try:
		engine = engine
		connection = connection
		metadata = MetaData()
		assignmnent = Table('assignment', metadata, autoload=True , autoload_with=engine)
		selectAssignmnent = select([assignmnent]).where(assignmnent.c.assignmentID == stringAssignmentID)
		returnValue =  list(connection.execute(selectAssignmnent))
	except:
		print traceback.print_exc()
	return returnValue	

def getStudentFromStudentTable(engine, connection, stringCourseID):
	returnValue = False
	try:
		engine = engine
		connection = connection
		metadata = MetaData()
		student = Table('student', metadata, autoload=True , autoload_with=engine)
		selectStudent = select([student]).where(student.c.studentID == stringStudentId)
		returnValue = list(connection.execute(selectStudent))
	except:
		print traceback.print_exc()
	return returnValue

def getStudent_settingFromStudentTable(engine, connection, stringStudentID):
	returnValue = False
	try:
		engine = engine
		connection = connection
		metadata = MetaData()
		student_settings = Table('student_settings', metadata, autoload=True , autoload_with=engine)
		select_student_settings = select([student_settings]).where(student_settings.c.studentID == stringStudentID)
		returnValue = list(connection.execute(select_student_settings))
	except:
		print traceback.print_exc()
	return returnValue

def updateStudent_assignment(engine, connection, stringStudentID,stringAssignmentID):
	returnValue = False
	try:
		engine = engine
		connection = connection
		metadata = MetaData()
		student_assignment = Table('student_assignment', metadata, autoload=True , autoload_with=engine)
		update = student_assignment.update(student_assignment).where(student_assignment.c.studentID==stringStudentId).values()
		student_settings = Table('student_assignment', metadata, autoload=True , autoload_with=engine)
		select_student_settings = select([student_settings]).where(student_settings.c.studentID == stringStudentID)
		returnValue = list(connection.execute(select_student_settings))
	except:
		print traceback.print_exc()
	return returnValue