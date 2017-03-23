import sys
sys.path.append("../databasehandler")
from connectHerokuMYSQL import getAllEntriesFromStudentTable

#returns a List of lists [[userid,refreshToken]]
def getAllUserReffreshTokens(engine,connection):
	returnList =[]

	studententries = getAllEntriesFromStudentTable(engine, connection)
	for students in studententries:
		tempList=[]
		tempList.append(students[0])
		tempList.append(students[3])
		returnList.append(tempList)
	return returnList
	
#getAllUserReffreshTokens()

def getAllUsers(engine,connection):
	returnList =[]
	studententries = getAllEntriesFromStudentTable(engine, connection)
	for students in studententries:
		tempList=[]
		for entries in students:
			tempList.append(entries)
		returnList.append(tempList)
	return returnList

def getAllCoursesForStudent(engine, connection,studentID):
	returnList=[]
	studenCourses = getEntriesFromStudent_courseTable(engine, connection,studentID)
	for entries in studenCourses:
		returnList.append(entries)
	return returnList

def getAllLecturesForStudent(engine,connection,courseID):
	returnList = []
	courses = getEntriesFromCourseTable(engine, connection,CourseId)
	for entries in courses:
		returnList.append(entries)
	return returnList

def getAllAssignmentsForStudent(engine,connection,stringCourseID):
	returnList = []
	assignments = getEntriesFromAssignment_courseTableReturnAssignments(engine,connection,stringCourseID)
	for entries in assignments:
		returnList.append(entries)
	return returnList
