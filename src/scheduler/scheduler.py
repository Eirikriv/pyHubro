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
	time = time[0:2] + time[3:5]
	return time	

def getEndTimeFromEvent(event): #gets the end time from an event recieved from getDayEvents
	endWithDate=event.split('E',1)[1]
	time=endWithDate.split('T',1)[1]
	time = time[0:2] + time[3:5]
	return time

def getEndTimeFromFirstEvent(event): #Gets the end time from the first event wich does not have the E letter in string
	time=event.split('T',1)[1]
	time = time[0:2] + time[3:5]
	return time

def addIntervallToTime(time,intervall):
	currenttime = datetime.datetime(2000,1,1,int(time[0:2]),int(time[2:4]),59,)
	if(intervall[0:2]!=''):
		addTime = datetime.timedelta(hours=int(intervall[0:2]))
		currenttime = currenttime + addTime
	if(int(intervall[2:4])!=0):
		addTime = datetime.timedelta(minutes=int(intervall[2:4]))
		currenttime = currenttime + addTime
	return currenttime.strftime("%H%M")

def checkIfEventFitsBetweenTwo(firstEvent,SecoundEvent,event): #forste to tar inn strenger, siste er en liste
	flagg=0
	if('E' in firstEvent):
		firstEventEndTime = getEndTimeFromEvent(firstEvent)
		firstEventEndTimeWithIntervall=addIntervallToTime(firstEventEndTime,"0005")
		endTimeForNewEvent=addIntervallToTime(firstEventEndTimeWithIntervall,event[5])
		if(endTimeForNewEvent<getStartTimeFromEvent(SecoundEvent)):
			flagg=1
			return [True,firstEventEndTimeWithIntervall,endTimeForNewEvent]

	else:
		firstEventEndTime = getEndTimeFromFirstEvent(firstEvent)
		endTimeForNewEvent=addIntervallToTime(firstEventEndTime,event[5])
		print(firstEventEndTime)
		if(endTimeForNewEvent<getStartTimeFromEvent(SecoundEvent)):
			flagg=1
			return [True,getStartTimeFromEvent(firstEvent),endTimeForNewEvent]
	if(flagg==0):
		return [False,None,None]

def getDayEvents(date, daysAhead, earliestStart, latestEnd): #date on form YYYY-DD-MM
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    # now = datetime.datetime.utcnow().isoformat() + 'Z' 'Z' indicates UTC time
    dateStart = ofsetDateByANumberOfDays(date,-1)
    dateStart = date + "T" + "23:59:00Z"
    dateEnd = ofsetDateByANumberOfDays(date,daysAhead)
    eventsResult = service.events().list(
        calendarId='primary', timeMin=dateStart, timeMax=dateEnd,maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if not events:
        print('No upcoming events found.')
    listeMedEvents=[]
    listeMedEvents.append(earliestStart)
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date')) #Automaticly adds a space in between the fields
        end = event['end'].get('dateTime', event['end'].get('date'))
        appendString = start[0:16] +'E' + end[0:16]
        listeMedEvents.append(appendString)
    listeMedEvents.append(latestEnd)
    return listeMedEvents

#events on the form: [title,startdate,endate,starttime,endtime,duration,description,place]
def createAndExecuteEvent(event):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    beskrivelse=event[6]
    sted=event[7]
    startdato=event[1]
    sluttdato=event[2]
    starttid=event[3]
    sluttid=event[4]
    if event[6]==None:
    	beskrivelse=""
    if event[7]==None:
      sted=""
    event = {
      'summary': event[0],
      'location': sted,
      'description': beskrivelse,
      'start': {
        'dateTime': startdato[0:4]+'-'+startdato[4:6]+'-'+startdato[6:8]+'T'+starttid[0:2]+':'+starttid[2:4]+':'+'00',
        'timeZone': 'Europe/Oslo',
      },
      'end': {
        'dateTime': sluttdato[0:4]+'-'+sluttdato[4:6]+'-'+sluttdato[6:8]+'T'+sluttid[0:2]+':'+sluttid[2:4]+':'+'00',
        'timeZone': 'Europe/Oslo',
      },
      'reminders': {
        'useDefault': True,#Reminder not implemented yet
      },
    }
    event = service.events().insert(calendarId='primary', body=event).execute() #executes the current event
#events on the form: [title,startdate,endate,starttime,endtime,duration,description,place]
def insertEvent(event):
  createAndExecuteEvent(event)
#events on the form: [title,startdate,endate,starttime,endtime,duration,description,place]
def insertEventIfAwalibleTimeOnThatDate(date, event, earliestStart, latestEnd):#loops thru the day, inserts the event if time is found
	eventList=getDayEvents(date, earliestStart, latestEnd)
	flagg=0
	print(eventList)
	for n in range(len(eventList)-1):
		currentEvent=eventList[n]
		nextEvent=eventList[n+1]
		slotIfAvalibleSpot=checkIfEventFitsBetweenTwo(currentEvent,nextEvent,event)
		if(slotIfAvalibleSpot[0]==True):
			event[1]=date
			event[2]=date
			event[3]=slotIfAvalibleSpot[1]
			event[4]=slotIfAvalibleSpot[2]
			createAndExecuteEvent(event)
			flagg=1
			print("sucessfully found a slot for your appointment")
			break
		else:
			continue



def createEvent(tittel,stardato,sluttdato,starttid,sluttid,varighet,typE,beskrivelse,sted):
	returnList=[tittel,stardato,sluttdato,starttid,sluttid,varighet,typE,beskrivelse,sted]
	return returnList

def incrementDate(date):
  date=datetime.datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),12,30,00)
  date+=datetime.timedelta(days=1)
  return date.strftime("%Y%m%d")



#TestData
date="20170201"
event=['Lese strategi','','','','','0200','','Strategi TIO4265','Kjel2','1']
firstEventOfDay=['S2017-02-01T08:00']
earliestStart='S2016-11-04T08:00'
latestEnd='S2016-11-04T22:58E2016-11-04T22:59'
#End Test Data
#def main(date,event,earliestStart,latestEnd):
#  insertEventIfAwalibleTimeOnThatDate(date,event,earliestStart,latestEnd)

##OldTestData
# print(incrementDate("20161105"))
#analysere med google analytics nettstedtrafikk, inn og ut pa buss og tbane folk vilf finne vite naar man kan ta gjennomsnitt
#def makeDayScheduleDynamic():#Before this, implement priority in events and "static event"
#returnerer liste [True,starttid,sluttid]
#insertEventIfAwalibleTimeOnThatDate(date,event)
#eventList=['2016-02-01T10:15E2016-11-04T18:10','2016-11-04T16:15E2016-11-04T17:00','2016-11-04T20:00E2016-11-04T22:00']
#events on the form: [tittel,stardato,sluttdato,starttid,sluttid,varighet,beskrivelse,sted]
#alle tidspunkt paa formen TTMM
#alle datoer paa formen AAAAMMDD
#insertEventIfAwalibleTimeOnThatDate(date,event,earliestStart,latestEnd)
##EndOldTestdata









