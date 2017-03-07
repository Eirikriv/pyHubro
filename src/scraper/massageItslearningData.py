import time
#Converts to the form: [AssimentDetails, CourseName, deadline date, deadline time]

def monthConverter(monthAsString):
    months=["januar","februar","mars","april","mai","juni","juli","august","september","oktober","november","desember"]
    returnVar = 0
    for n in range(len(months)):
        if months[n]==monthAsString:
            returnVar = n + 1 
            break
    if(returnVar==0):
        returnVar = "00" 
    return str(returnVar)

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def getDateOnRightFormat(day): 
    
    try: 
        len(day)
        returnVar = ""
        if len(day) > 3:
            returnVar = "00"
        else:
            for words in day:
                if(isNumber(words)):
                    returnVar = returnVar+words
            if len(returnVar)==1:
                returnVar = "0"+returnVar
            elif(len(returnVar)==2):
                None
            else:
                returnVar="00"   
    except:
        returnVar="00"
    return returnVar


def prepDeliveriesForDatabase(rawScrapeFromIts): #converts to applicable databaseformat, returns on formate:
    returnList=[]      
    try:                          #[assingmentdetails, coursename, date, time]
        assigmentDetailsSting = rawScrapeFromIts[0]
        assigmnentDetails = assigmentDetailsSting.split()
        crDetails = ""
        for n in range(0,len(assigmnentDetails)):
            crDetails=crDetails+" "+assigmnentDetails[n]
            if n == 1:
                break
        returnList.append(crDetails)

        courseNameString = rawScrapeFromIts[1]
        courseName = courseNameString.split()
        name = courseName[0:len(courseName)-2]
        crName=""
        for words in name:
            crName = crName + " "+ words 
        returnList.append(crName)

        deadLineDetailsString = rawScrapeFromIts[2]
        deadLineDetails = deadLineDetailsString.split()
        day = getDateOnRightFormat(deadLineDetails[1])
        month=monthConverter(deadLineDetails[2])

        month=getDateOnRightFormat(month)


        year = deadLineDetails[3]
        dateString = year + "-" + month + "-" + day
        returnList.append(dateString)

        time = deadLineDetails[4]
        time = time + ":00"

        returnList.append(time)
    except:
        returnList = ['', '', '00-00-00', '00:00:00']
    return returnList


def prepAllDeiveriesForDatabase(totalDeliveryList): #prepares for all assingments found on itslearning
    returnList = []
    for deliveries in totalDeliveryList:
        returnList.append(prepDeliveriesForDatabase(deliveries))
    return returnList
