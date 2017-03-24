
import unicodedata
from datetime import datetime, timedelta


def OwlbrainScheduler(assignmentDeadline, initialHoursSet, calendarEvents):

    assignmentDeadline = datetime.strptime(assignmentDeadline, '%Y-%m-%d %H:%M:%S')
    remainingWorkLengthInQuarters = initialHoursSet * 4
    calendarEvents = [unicodedata.normalize('NFKD', x).encode('ascii', 'ignore') for x in calendarEvents]
    assignedWorkSlots = []

    currentDayInSearch = 2         # antall dager for frist forst testet for ledig tid
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
            quartersCurrentDayInSearch[startQuarter-1] = 1

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
        #TODO: pick the longest free slot in a day first
        #TODO: put a buffer of a quarter before next events

        currentDayInSearch += (currentDayInSearchCounter * currentDayInSearchInverter)
        currentDayInSearchCounter += 1
        currentDayInSearchInverter *= -1

    return assignedWorkSlots

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

    if not freeQuarters:
        return []+[]
    else:
        startFreeQuarters = [freeQuarters[0]]

        for lengths in slotLengths[:-1]:
            startFreeQuarters.append(freeQuarters[lengths])

    return [startFreeQuarters]+[slotLengths]

def newWorkSlot(currentDateInSearch, freeSlot, slotLength):
    startTime = datetime.strptime(("0" + str(int(freeSlot) / 4))[-2:] + ":" +
                                  ("0" + str((int(freeSlot) % 4) * 15))[-2:] + ":00", '%H:%M:%S')
    endTime = startTime + \
              timedelta(0, slotLength * 15 * 60)
    newWorkSlot = [startTime.strftime('%H:%M:%S'), endTime.strftime('%H:%M:%S'), currentDateInSearch]
    return newWorkSlot