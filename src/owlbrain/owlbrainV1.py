
import unicodedata
from datetime import datetime, timedelta

#TODO Eirik -> Lage funksjon som henter ut og setter inn database
#Hvordan bor output fra databasen vare?
#eks: [userID,date , listOFEntriesThatDate]
#listOfEntriesThatDate :[[type, id, starttime, endtime],[type, id, starttime, endtime],[type, id, starttime, endtime]]
#eks: ["0001",2017-03-07,["assignement","0001","23:59:00","23:59:00"],["lecture","0002","08:15:00","10:00:00"]]


#Kan funksjonen kanskje returnere paa samme format? saa kan jeg sett inn i DB med omtrendt samme metoder


# PSUDO CODE
# EVENT: new assignment given
# For all students taking this course:
# Run this code and input studentID, courseName, assigmentTitle and assignment deadline
assignmentDeadline = datetime.strptime('2017-03-20 23:59:59', '%Y-%m-%d %H:%M:%S')
#
# Owlbrain asks database for the student initial hours for assignments in this course
initialHoursSet = 3
remainingWorkLength = initialHoursSet
# Owlbrain asks the calender for event from the deadline and 11 days back
#
calendarExport = [u'2017-03-14T08:15:00EB2017-03-14T10:00:00', u'2017-03-14T10:00:00EB2017-03-14T14:00:00', u'2017-03-14T12:15:00EB2017-03-14T15:00:00', u'2017-03-14T16:15:00EB2017-03-14T18:00:00', u'2017-03-15T08:15:00EB2017-03-15T16:00:00', u'2017-03-16T08:30:00EB2017-03-16T16:00:00', u'2017-03-16T11:57:00EB2017-03-16T12:00:00', u'2017-03-16T15:15:00EB2017-03-16T18:00:00', u'2017-03-16T17:15:00EB2017-03-16T19:00:00']
calendarExport = [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in calendarExport]
print calendarExport
#
#
currentDaySearch = 6         #Prior er seks dager for frist
currentDaySearchCounter = 1
currentDaySearchInverter = 1

#while currentDaySearch != 12:

listQuartersInADay = [0] * (24 * 4)         #bitstring with 24*4 zero-entries, one for each quarter in a day
listQuartersInADay[:(8 * 4)] = [1] * (8 * 4)        #won't work before 8am
listQuartersInADay[-(4 * 4):] = [1] * (4 * 4)        #won't work after 8am

currentDay = datetime.strftime((assignmentDeadline - timedelta(days=currentDaySearch)).date(), '%Y-%m-%d')

eventsOnThisDay = [x for x in calendarExport if x[0:10] == currentDay]

for events in eventsOnThisDay:
    startQuarter = int(events[11:13])*4 + int(int(events[14:16])/15)
    eventLength = int(events[32:34])*4 + int(int(events[35:37])/15) - startQuarter

    listQuartersInADay[startQuarter:startQuarter + eventLength] = [1] * eventLength

print listQuartersInADay

for quarters in listQuartersInADay:
    #find index of the first quarter in a series of at least four free quarters
    # and how many free quarters there are in the series

#assign working time in the longest series of free quarters until remainingWorkLenght = 0
#If there aren't enough free quarters, test the next day


    #DO stuff
    # Sort all busy events on this day with regards to start time, stored in linked list or equivalent
    # Traverse through list
    #     look at start time and end time and turn all allfected bits (if not allready turned on)
    #         Plus one quarter if the event lasts for 4 quarters or more
#
#
# Gaa gjennom bitstrengen fra start og finn forste ledige okt lengre enn 1 time
#     Hvis den finnes
#         Lag en arbeidsokt i den ledige tiden, maks saa mange timer som gjenstaar
#     Hvis den ikke finnes
#         Dag = Dag + inverter*counter
#         counter++
#         inverter = -inverter
#         Gaa til Dag

