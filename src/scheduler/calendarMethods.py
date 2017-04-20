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
import time
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
sys.path.append("../databasehandler")
from databaseUtils import *
from clientID_clientSecret import CLIENT_ID , CLIENT_SECRET
import datetime as dt

def findDaysBetweenDates(date):
    current = dt.date.today()
    future = dt.date(int(date[0:4]), int(date[5:7]) , int(date[8:10]))
    delta = future - current
    return delta.days

def ofsetDateByANumberOfDays(dateYYYYdashMMdashDD, daysoffset): #"-" between YYYY-DD, negative day brings you backvards in time
  offsetDate = ""
  date = datetime.datetime(int(dateYYYYdashMMdashDD[0:4]), int(dateYYYYdashMMdashDD[5:7]) , int(dateYYYYdashMMdashDD[8:10]), 18, 00)
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
  listeMedEvents=False
  try:
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
  except:
    None
  return listeMedEvents
def createAndExecuteEvent(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,colorId,http):
    returnValue = False
    try:
      http = http
      service = discovery.build('calendar', 'v3', http=http)
      calId=""
      if beskrivelse==None:
      	beskrivelse=""
      if sted==None:
        sted=""
      event = {
        'id': "some", 
        'summary': tittel,
        'location': sted,
        'description': beskrivelse,
        'colorId' : colorId,
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
      calId = checkIfHubroCalExist(service)
      if(calId!=None):
        None
      else:
        calId = createHubroCalendar(service)
        print(calId)
      time.sleep(2)
      event = service.events().insert(calendarId=calId, body=event).execute() #executes the current event
      returnValue = True
    except:
      None
    return returnValue
#refreshToken = "1/I2bJkHp2xg0HHD176-8EdiJR4wQLZQp2D0EL7q1BNoo"
#print(refreshToken)
#credentials = authorise(CLIENT_ID,CLIENT_SECRET,refreshToken)
#print(getDayEvents("2017-03-17","23:59:00","2",credentials))

def checkIfHubroCalExist(service):
  page_token = None
  returnValue = None
  while returnValue==None:
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      print(calendar_list_entry['summary'])
      if(calendar_list_entry['summary']=='hubro'):
        returnValue = calendar_list_entry['id']
        break
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break
  return returnValue

def createHubroCalendar(service):
  calendar = {
    'summary': 'hubro',
    'timeZone': 'Europe/Oslo'
}
  created_calendar = service.calendars().insert(body=calendar).execute()
  return created_calendar['id']

def insertEventToCal(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted, colorID,refreshToken):
  http = authorise(CLIENT_ID,CLIENT_SECRET,refreshToken)
  createAndExecuteEvent(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted,colorID,http)
  return True

def getEventsDaysBack(date, time ,daysBack,refreshToken):
  refreshToken = refreshToken
  http = authorise(CLIENT_ID,CLIENT_SECRET,refreshToken)
  return getDayEvents(date,time,daysBack,http)

# def test():
#   insertEventToCal("dra til tokyo","2017-03-30","2017-03-30","08:30:00","10:00:00","goin on a trip hubro says","Verneas","6")
# test()
