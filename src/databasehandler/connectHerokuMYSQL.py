from sqlalchemy import create_engine, MetaData,Table, select
import os
from databaseConnectDetails import *
from sqlalchemy.orm import sessionmaker

username = unameHeroku
password = passwordHeroku
URI = 'mysql://'+str(username)+':'+str(password)+'@us-cdbr-iron-east-04.cleardb.net/heroku_f8b7f102c73b268'


def insertStudentIntoDatabase(engine, connection,stringStudentID,stringStudentName):
	engine = engine
	connection = connection
	metadata = MetaData()
	student = Table('student', metadata, autoload=True , autoload_with=engine)
	ins = student.insert()
	new_student = ins.values(studentID=stringStudentID,studentName=stringStudentName)
	connection.execute(new_student)	


def getEntryFromStudentTable(engine, connection,stringStudentId):
	engine = engine
	connection = connection
	metadata = MetaData()
	student = Table('student', metadata, autoload=True , autoload_with=engine)
	selectStudent = select([student]).where(student.c.studentID == stringStudentId)
	for row in connection.execute(selectStudent):
		return row

def insertStudent_courseIntoDatabase(engine, connection,stringStudentID,stringCourseID):
	engine = engine
	connection = connection
	metadata = MetaData()
	studentCourse = Table('student_course', metadata, autoload=True , autoload_with=engine)
	#print(metadata.tables.keys())
	ins = studentCourse.insert()
	new_studentCourse = ins.values(studentID=stringStudentID,courseID=stringCourseID)
	connection.execute(new_studentCourse)
#insertStudent_courseIntoDatabase("0001","0001")

def getEntriesFromStudent_courseTable(engine, connection,stringStudentId):
	engine = engine
	connection = connection
	metadata = MetaData()
	student_course = Table('student_course', metadata, autoload=True , autoload_with=engine)
	selectStudent = select([student_course]).where(student_course.c.studentID == stringStudentId)
	return list(connection.execute(selectStudent))
	
#print(getEntryFromStudent_courseTable("0001"))

def insertACourseIntoDatabase(engine, connection,stringCourseID,stringCourseName):
	engine = engine
	connection = connection
	metadata = MetaData()
	course = Table('course', metadata, autoload=True , autoload_with=engine)
	#print(metadata.tables.keys())
	ins = course.insert()
	new_course = ins.values(courseID=stringCourseID,courseName=stringCourseName)
	connection.execute(new_course)
#insertCourseIntoDatabase("0001","TDT4140")

def getEntriesFromCourseTable(engine, connection,stringCourseId):
	engine = engine
	connection = connection
	metadata = MetaData()
	course = Table('course', metadata, autoload=True , autoload_with=engine)
	selectCourse = select([course]).where(course.c.courseID == stringCourseId)
	return list(connection.execute(selectCourse))
	
#print(getEntryFromCourseTable("0001"))
def insertAssignmentIntoDatabase(engine, connection, stringAssigmentID,stringAssignmentDate,stringAssignmentTime, stringAssignmentDescription):
	engine = engine
	connection = connection
	metadata = MetaData()
	assignmnent = Table('assignment', metadata, autoload=True , autoload_with=engine)
	#print(metadata.tables.keys())
	ins = assignmnent.insert()
	new_assignmnent = ins.values(assignmentID=stringAssigmentID,assignmnentDate=stringAssignmentDate,assignmnentTime=stringAssignmentTime,assignmentDescription=stringAssignmentDescription)
	connection.execute(new_assignmnent)
#insertAssignmnentIntoDatabase("0001","2017-01-01","23:59:00")

def getEntryFromAssigmnentTable(engine, connection,stringAssignmentID):
	engine = engine
	connection = connection
	metadata = MetaData()
	assignmnent = Table('assignment', metadata, autoload=True , autoload_with=engine)
	selectAssignmnent = select([assignmnent]).where(assignmnent.c.assignmentID == stringAssignmnentID)
	for row in connection.execute(selectAssignmnent):
		return row
#print(getEntryFromAssignmnentTable("0001"))

def getLastEntryFromAssignmentTable(engine, connection):
	engine = engine
	connection = connection
	metadata = MetaData()
	assignmnent = Table('assignment', metadata, autoload=True , autoload_with=engine)
	selectAssignment=select([assignmnent])
	result = connection.execute(selectAssignment)
	result =list(result)
	return result[-1]

def insertLecturesIntoDatabase(engine, connection, stringLectureID,stringLectureDate,stringLectureStartTime,stringLectureEndTime,stringLectureDescription,stringLectureLocation):
	engine = engine
	connection = connection
	metadata = MetaData()
	lecture = Table('lecture', metadata, autoload=True , autoload_with=engine)
	#print(metadata.tables.keys())
	ins = lecture.insert()
	new_lecture = ins.values(lectureID=stringLectureID,lectureDate=stringLectureDate,lectureStartTime=stringLectureStartTime,lectureEndTime=stringLectureEndTime,lectureDescription=stringLectureDescription,lectureLocation=stringLectureLocation)
	connection.execute(new_lecture)
#insertLectureIntoDatabase("0001","2017-01-01","08:15:00","10:00:00","Two hour lecture in Databases","R1")

def getEntryFromLectureTable(engine, connection,stringLectureID):
	engine = engine
	connection = connection
	metadata = MetaData()
	lecture = Table('lecture', metadata, autoload=True , autoload_with=engine)
	selectLecture = select([lecture]).where(lecture.c.lectureID == stringLectureID)
	for row in connection.execute(selectLecture):
		return row

def getLastEntryFromLectureTable(engine, connection):
	engine = engine
	connection = connection
	metadata = MetaData()
	lecture = Table('lecture', metadata, autoload=True , autoload_with=engine)
	selectLecture=select([lecture])
	result = connection.execute(selectLecture)
	result =list(result)
	return result[-1]

def getEntriesFromLectureTable(engine, connection,stringLectureID):
	engine = engine
	connection = connection
	metadata = MetaData()
	lecture = Table('lecture', metadata, autoload=True , autoload_with=engine)
	selectLecture = select([lecture]).where(lecture.c.lectureID == stringLectureID)
	returnList=[]
	for row in connection.execute(selectLecture):
		returnList.append(row)
	return returnList

def insertLecture_courseIntoDatabase(engine, connection,stringLectureID,stringCourseID):
	engine = engine
	connection = connection
	metadata = MetaData()
	lecture_course = Table('lecture_course', metadata, autoload=True , autoload_with=engine)
	ins = lecture_course.insert()
	new_lecture_course = ins.values(lectureID=stringLectureID,courseID=stringCourseID)
	connection.execute(new_lecture_course)

#insertLecture_courseIntoDatabase("0001","0001")
def getEntryFromLecture_courseTable(engine, connection,stringLectureID):
	engine = engine
	connection = connection
	metadata = MetaData()
	lecture_course = Table('lecture_course', metadata, autoload=True , autoload_with=engine)
	selectLecture = select([lecture_course]).where(lecture_course.c.lectureID == stringLectureID)
	for row in connection.execute(selectLecture):
		return row

def insertAssignment_courseIntoDatabase(engine, connection, stringAssignmentID,stringCourseID):
	engine = engine
	connection = connection
	metadata = MetaData()
	assignment_course = Table('assignment_course', metadata, autoload=True , autoload_with=engine)
	#print(metadata.tables.keys())
	ins = assignment_course.insert()
	new_assignment_course = ins.values(assignmentID=stringAssignmentID,courseID=stringCourseID)
	connection.execute(new_assignment_course)
#insertAssignment_courseIntoDatabase("0001","0001")

def getEntryFromAssignment_courseTable(engine, connection,stringAssignmentID):
	engine = engine
	connection = connection
	metadata = MetaData()
	assignment_course = Table('assignment_course', metadata, autoload=True , autoload_with=engine)
	selectLecture_course = select([assignment_course]).where(assignment_course.c.assignmentID == stringAssignmentID)
	for row in connection.execute(selectLecture_course):
		return row
#print(getEntryFromAssignment_courseTable("0001"))

def getAllEntriesFromStudentTable(engine, connection):
	engine = engine
	connection = connection
	Session = sessionmaker()
	Session.configure(bind=engine)
	metadata = MetaData()
	Session = Session()
	student = Table('student', metadata, autoload=True , autoload_with=engine)
	return list(Session.query(student).all())

