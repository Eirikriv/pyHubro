#imports to manage google calendar api
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
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def ofsetDateByANumberOfDays(dateYYYYMMDD, daysoffset): #"-" between YYYY-DD, negative day brings you backvards in time
  offsetDate = ""
  date = datetime.datetime(int(dateYYYYMMDD[0:4]), int(dateYYYYMMDD[5:7]) , int(dateYYYYMMDD[8:10]), 18, 00)
  DD = datetime.timedelta(days=daysoffset)
  offsetDate = date + DD
  offsetDate = offsetDate.isoformat()
  return offsetDate[0:10]

def get_credentials(): #required to connect to google calendar API
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getStartTimeFromEvent(event): #gets the start time from an event recieved from getDayEvents
	endWithDate=event.split('E',1)[0]
	time=endWithDate.split('T',1)[1]
	time = time[0:2] + ":"+time[3:5] +":" + time[6:8]
	return time	

def getEndTimeFromEvent(event): #gets the end time from an event recieved from getDayEvents
	endWithDate=event.split('E',1)[1]
	time=endWithDate.split('T',1)[1]
	time = time[0:2] + ":"+time[3:5] +":" + time[6:8]
	return time

def getEndTimeFromFirstEvent(event): #Gets the end time from the first event wich does not have the E letter in string
	time=event.split('T',1)[1]
	time = time[0:2] + ":"+time[3:5] +":" + time[6:8]
	return time

def addIntervallToTime(time,intervall):
	currenttime = datetime.datetime(2000,1,1,int(time[0:2]),int(time[3:5]),59,)
	if(intervall[0:2]!=''):
		addTime = datetime.timedelta(hours=int(intervall[0:2]))
		currenttime = currenttime + addTime
	if(int(intervall[3:5])!=0):
		addTime = datetime.timedelta(minutes=int(intervall[3:5]))
		currenttime = currenttime + addTime
	returnVar = currenttime.strftime("%H%M") + ":00"
	returnVar = returnVar[0:2] + ":" + returnVar[2:len(returnVar)]
	return returnVar

#print()checkIfEventFitsBetweenTwo('2017-03-16T09:30:00E2017-03-16T11:00:00','2017-03-16T14:30:00E2017-03-16T16:00:00',"02:00:00","00:05:00"))

def getDayEvents(date, time ,daysBack): #date on form YYYY-DD-MM
    credentials = get_credentials()
    daysBack = int(daysBack)
    daysBack =  -daysBack-1
    http = credentials.authorize(httplib2.Http())
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


#events on the form: [title,startdate,endate,starttime,endtime,duration,description,place]
def createAndExecuteEvent(tittel,startdato,sluttdato,starttid,sluttid,beskrivelse,sted):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
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

def demo(date,time,daysBack,tittel,eventstardato,eventsluttdato,eventstarttid,eventsluttid,beskrivelse,sted):
  print(getDayEvents(date,time,daysBack))
  createAndExecuteEvent(tittel,eventstardato,eventsluttdato,eventstarttid,eventsluttid,beskrivelse,sted)
demo("2017-03-17","23:59:00","2","HubroTest","2017-03-17","2017-03-17","16:15:00","17:00:00","Write a paragraph","Your favorite studyplace") 


#events on the form: [title,startdate,endate,starttime,endtime,duration,description,place]
#('Lekse','Lese TDT4100','02:00:00',"2017-03-26","10","Your studyplace","08:15:00","17:00:00")
