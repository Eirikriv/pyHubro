import sys
sys.path.append("../databasehandler")
from connectHerokuMYSQL import getAllEntriesFromStudentTable

#returns a List of lists [[userid,refreshToken]]
def getAllUserReffreshTokens():
	returnList =[]

	studententries = getAllEntriesFromStudentTable()
	for students in studententries:
		tempList=[]
		tempList.append(students[0])
		tempList.append(students[3])
		returnList.append(tempList)
	return returnList
	
getAllUserReffreshTokens()

