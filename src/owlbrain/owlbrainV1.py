#TODO Eirik -> Lage funksjon som henter ut og setter inn database
#Hvordan bor output fra databasen vare?
#eks: [userID,date , listOFEntriesThatDate]
#listOfEntriesThatDate :[[type, id, starttime, endtime],[type, id, starttime, endtime],[type, id, starttime, endtime]]
#eks: ["0001",2017-03-07,["assignement","0001","23:59:00","23:59:00"],["lecture","0002","08:15:00","10:00:00"]]


#Kan funksjonen kanskje returnere paa samme format? saa kan jeg sett inn i DB med omtrendt samme metoder


# PSUDO CODE
#
# input <- kalender fra og med frist til og med 11 dager for frist
# input <- oktstart og lengde
#
currentDaySearch = 6         #Prior er seks dager for frist
currentDaySearchCounter = 1
currentDaySearchInverter = 1

listRepresentingQuartersInADay = [0] * 24 * 4         #bitstring with 24*4 zero-entries, one for each quarter in a day

listRepresentingQuartersInADay[:8 * 4] = [1] * (8 * 4)        #won't work before 8am
listRepresentingQuartersInADay[8 * 4:] = [1] * (8 * 4)        #won't work after 8am



# Sort all busy events on this day with regards to start time, stored in linked list or equivalent
# Traverse through list
#     look at start time and end time and turn all allfected bits (if not allready turned on)
#         Plus one quarter if the event lasts for 4 quarters or more
#
#     Remaining_work_length = Initial_work_length
#
# Gaa gjennom bitstrengen fra start og finn forste ledige okt lengre enn 1 time
#     Hvis den finnes
#         Lag en arbeidsokt i den ledige tiden, maks saa mange timer som gjenstaar
#     Hvis den ikke finnes
#         Dag = Dag + inverter*counter
#         counter++
#         inverter = -inverter
#         Gaa til Dag

