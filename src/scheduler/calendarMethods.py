from __future__ import print_function
import httplib2
import os
import traceback
import sys
sys.path.insert(1, '/Library/Python/2.7/site-packages')
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
#imports to manage the client secret of google calendar
import traceback
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
from oauth2client.client import AccessTokenCredentials
from oauth2client import client, GOOGLE_TOKEN_URI, GOOGLE_REVOKE_URI
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
sys.path.append("../databasehandler")
from connectHerokuMYSQL import getAllEntriesFromStudentTable
from clientID_clientSecret import CLIENT_ID , CLIENT_SECRET

#returns a List of lists [[userid,refreshToken]]
def getAllUserReffreshTokens():
	returnList =[]

	studententries = getAllEntriesFromStudentTable()
	for students in studententries:
		tempList=[]
		tempList.append(students[0])
		tempList.append(students[4])
		returnList.append(tempList)
	return returnList

def ofsetDateByANumberOfDays(dateYYYYMMDD, daysoffset): #"-" between YYYY-DD, negative day brings you backvards in time
  offsetDate = ""
  date = datetime.datetime(int(dateYYYYMMDD[0:4]), int(dateYYYYMMDD[5:7]) , int(dateYYYYMMDD[8:10]), 18, 00)
  DD = datetime.timedelta(days=daysoffset)
  offsetDate = date + DD
  offsetDate = offsetDate.isoformat()
  return offsetDate[0:10]	

def authorise(clientID,clientSecret,refreshToken):
	CLIENT_ID = clientID
	CLIENT_SECRET = clientSecret
	REFRESH_TOKEN = refreshToken
	credentials = client.OAuth2Credentials(None, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, None, GOOGLE_TOKEN_URI,None, revoke_uri=GOOGLE_REVOKE_URI)
	# refresh the access token (or just try using the service)
	credentials.refresh(httplib2.Http())
	http = credentials.authorize(httplib2.Http())
	credentials.refresh(http)
	return http

def getDayEvents(date, time ,daysBack,http):
    daysBack = int(daysBack)
    daysBack =  -daysBack-1
    service = discovery.build('calendar', 'v3', http=http)
    dateStart = ofsetDateByANumberOfDays(date,(daysBack))
    dateStart = dateStart + "T" + "00:00:00Z"
    dateEnd = ofsetDateByANumberOfDays(date,-1)
    dateEnd = dateEnd + "T" + time +"Z"
    print(dateStart,dateEnd)
    eventsResult = service.events().list(
        calendarId='primary', timeMin=dateStart, timeMax=dateEnd,maxResults=300, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if not events:
        print('No upcoming events found.')
    listeMedEvents=[]
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date')) #Automaticly adds a space in between the fields
        end = event['end'].get('dateTime', event['end'].get('date'))
        appendString = start[0:19] +'EB' + end[0:19]
        listeMedEvents.append(appendString)
    return listeMedEvents

def createAndExecuteEvent(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,http):
    http = http
    service = discovery.build('calendar', 'v3', http=http)
    if beskrivelse==None:
    	beskrivelse=""
    if sted==None:
      sted=""
    event = {
      'summary': tittel,
      'location': sted,
      'description': beskrivelse,
      'start': {
        'dateTime': startdato+"T"+starttid,
        'timeZone': 'Europe/Oslo',
      },
      'end': {
        'dateTime': sluttdato+"T"+sluttid,
        'timeZone': 'Europe/Oslo',
      },
      'reminders': {
        'useDefault': True,#Reminder not implemented yet
      },
    }
    event = service.events().insert(calendarId='primary', body=event).execute() #executes the current event

refreshToken = getAllUserReffreshTokens()[0][1]
print(refreshToken)
credentials = authorise(CLIENT_ID,CLIENT_SECRET,refreshToken)
print(getDayEvents("2017-03-17","23:59:00","2",credentials))