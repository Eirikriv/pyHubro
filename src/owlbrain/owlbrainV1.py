#TODO Eirik -> Lage funksjon som henter ut og setter inn database
#Hvordan bor output fra databasen vare?
#eks: [userID,date , listOFEntriesThatDate]
#listOfEntriesThatDate :[[type, id, starttime, endtime],[type, id, starttime, endtime],[type, id, starttime, endtime]]
#eks: ["0001",2017-03-07,["assignement","0001","23:59:00","23:59:00"],["lecture","0002","08:15:00","10:00:00"]]


#Kan funksjonen kanskje returnere paa samme format? saa kan jeg sett inn i DB med omtrendt samme metoder


# PSUDO CODE
#
# input <- kalender fra og med frist til og med 11 dager før frist
# input <- øktstart og lengde
#
# Dag = 6         #Prior er seks dager før frist
# inverter = 1
# counter = 1
#
# Create a bitstring with 12*4 zero-entries #length of worikng day should be modifiable
# Sort all busy events on this day with regards to start time, stored in linked list or equivalent
# Traverse through iist
#     look at start time and end time and turn all allfected bits (if not allready turned on)
#         Plus one quarter if the event lasts for 4 quarters or more
#
#     Remaining_work_length = Initial_work_length
#
# Gå gjennom bitstrengen fra start og finn første ledige økt lengre enn 1 time
#     Hvis den finnes
#         Lag en arbeidsøkt i den ledige tiden, maks så mange timer som gjenstår
#     Hvis den ikke finnes
#         Dag = Dag + inverter*counter
#         counter++
#         inverter = -inverter
#         Gå til Dag

