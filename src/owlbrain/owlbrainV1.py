
import unicodedata
from datetime import datetime, timedelta

# PSUDO CODE
# EVENT: new assignment given
# For all students taking this course:
# Run this code and input assignment deadline

def OwlbrainSheduler(assignmentDeadline, initialHoursSet, calendarEvents):

    assignmentDeadline = datetime.strptime('2017-03-16 23:59:59', '%Y-%m-%d %H:%M:%S')
    remainingWorkLengthInQuarters = initialHoursSet * 4
    assignedWorkSlots = []

    calendarEvents = [u'2017-03-14T08:15:00EB2017-03-14T10:00:00', u'2017-03-14T10:00:00EB2017-03-14T14:00:00',
                      u'2017-03-14T12:15:00EB2017-03-14T15:00:00', u'2017-03-14T16:15:00EB2017-03-14T18:00:00',
                      u'2017-03-15T08:15:00EB2017-03-15T16:00:00', u'2017-03-16T08:30:00EB2017-03-16T16:00:00',
                      u'2017-03-16T11:57:00EB2017-03-16T12:00:00', u'2017-03-16T15:15:00EB2017-03-16T18:00:00',
                      u'2017-03-16T17:15:00EB2017-03-16T19:00:00']
    calendarEvents = [unicodedata.normalize('NFKD', x).encode('ascii', 'ignore') for x in calendarEvents]
    print calendarEvents

    currentDayInSearch = 2         #Prior, for frist
    currentDayInSearchCounter = 1
    currentDayInSearchInverter = 1

    while currentDayInSearch != 5 and remainingWorkLengthInQuarters > 0:

        quartersCurrentDayInSearch = [0] * (24 * 4)
        quartersCurrentDayInSearch[:(8 * 4)] = [1] * (8 * 4)
        quartersCurrentDayInSearch[-(4 * 4):] = [1] * (4 * 4)

        currentDateInSearch = datetime.strftime((assignmentDeadline - timedelta(days=currentDayInSearch)).date(), '%Y-%m-%d')

        eventsOnCurrentDayInSearch = [x for x in calendarEvents if x[0:10] == currentDateInSearch]

        for events in eventsOnCurrentDayInSearch:
            startQuarter = int(events[11:13])*4 + int(int(events[14:16])/15)
            eventLength = int(events[32:34])*4 + int(int(events[35:37])/15) - startQuarter

            quartersCurrentDayInSearch[startQuarter:startQuarter + eventLength] = [1] * eventLength

        print quartersCurrentDayInSearch

            # ut ser jeg for meg at den gir : [ [event1], [event2] , [event3].... ]
            # der event1 er for eksempel: [startid,sluttid,dato]
            # paa formen: [08:00:00,10:00:00,2017-03-23]

            # for quarters in listQuartersInADay:
            # find index of the first quarter in a series of at least four free quarters
                # and how many free quarters there are in the series

            #assign working time in the longest series of free quarters until remainingWorkLenght = 0
            #If there aren't enough free quarters, test the next day

        freeSlotsInCurrentDayInSearch = FindFreeSlots(quartersCurrentDayInSearch)[:]

        for freeSlot in freeSlotsInCurrentDayInSearch[0]:
            slotLength = freeSlotsInCurrentDayInSearch[1][freeSlotsInCurrentDayInSearch[0].index(freeSlot)]
            if remainingWorkLengthInQuarters >= slotLength:
                remainingWorkLengthInQuarters -= slotLength
                assignedWorkSlots.append(newWorkSlot(currentDateInSearch, freeSlot, slotLength))
            elif remainingWorkLengthInQuarters > 0:
                slotLength = remainingWorkLengthInQuarters
                remainingWorkLengthInQuarters = 0
                assignedWorkSlots.append(newWorkSlot(currentDateInSearch, freeSlot, slotLength))

        print assignedWorkSlots

        currentDayInSearch += (currentDayInSearchCounter * currentDayInSearchInverter)
        currentDayInSearchCounter += 1
        currentDayInSearchInverter *= -1

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

    return()

def FindFreeSlots(list):
    freeQuarters = []
    tempResult = []
    newElementFlag = 0
    slotLengths = [0]

    for ind in (i for i, e in enumerate(list) if e == 0):
        tempResult.append(int(ind))
        if len(tempResult) > 1 and tempResult[-1] != tempResult[-2] + 1:
            tempResult = [tempResult[-1]]
        if len(tempResult) > 3:
            if tempResult[0] not in freeQuarters:
                freeQuarters += tempResult[:]
                newElementFlag = 1
            if newElementFlag == 1:
                slotLengths.append(len(freeQuarters)-4-slotLengths[-1])
                newElementFlag = 0
            freeQuarters[freeQuarters.index(int(tempResult[0])):freeQuarters.index(tempResult[0]) + len(tempResult)] = tempResult[:]
    slotLengths = slotLengths[2:] + [len(freeQuarters)-slotLengths[-1]]

    startFreeQuarters = [freeQuarters[0]]

    for lengths in slotLengths[:-1]:
        startFreeQuarters.append(freeQuarters[lengths])

    print [startFreeQuarters]+[slotLengths]

    return [startFreeQuarters]+[slotLengths]

def newWorkSlot(currentDateInSearch, freeSlot, slotLength):
    startTime = datetime.strptime(("0" + str(int(freeSlot) / 4))[-2:] + ":" +
                                  ("0" + str((int(freeSlot) % 4) * 15)[-2:]) + ":00", '%H:%M:%S')
    endTime = startTime + \
              timedelta(0, slotLength * 15 * 60)
    newWorkSlot = [startTime.strftime('%H:%M:%S'), endTime.strftime('%H:%M:%S'), currentDateInSearch]
    return newWorkSlot


if __name__ == '__main__':
    OwlbrainSheduler(0, 3, 0)