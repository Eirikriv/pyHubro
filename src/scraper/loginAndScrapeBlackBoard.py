from selenium import webdriver
from pyvirtualdisplay import Display
from scrapingSiteCredentials import *
import traceback
import time

def getUsername(): #get NTNU Feide username from user
    u_username=unameBlackBoard
    return u_username

def getUserPassword(): #get NTNU Feide password from user
    u_password=passBlackBoard
    return u_password

def sleep(sleepTimer): #sleep selenium so pages can load before next action is taken
    time.sleep(sleepTimer)
    return 

def scrapeBlackBoard(sleepTimer):
    allDeliveriesList=[]
    try:
        display = Display(visible=0, size=(1200, 1000))
        display.start()
        u_username=getUsername()
        u_password=getUserPassword()
        driver=webdriver.Firefox()
        driver.get('http://www.instabart.no/') 
        pressend=driver.find_element_by_id("blackboard")
        sleep(sleepTimer)
        pressend.click()
	
        sleep(sleepTimer)
        el = driver.find_element_by_id('org')
        for option in el.find_elements_by_tag_name('option'):
            if(option.text == 'NTNU'):
                option.click() 
                break
        pressSubmit=driver.find_element_by_id("submit")
        pressSubmit.click()
        sleep(sleepTimer)
        its=driver.find_element_by_id("username")
        sleep(sleepTimer)
        its.send_keys(u_username) 

        passwd = driver.find_element_by_id("password")
        sleep(sleepTimer)
        passwd.send_keys(u_password)


        loginbutton = driver.find_element_by_class_name("submit")
        loginbutton.click()
        time.sleep(7)
        courses = driver.find_element_by_class_name("courseListing")
        elementList = courses.find_elements_by_tag_name("li")
        allDeliveriesList = []
        for n in range(0,len(elementList)):
            print (len(elementList))
            driver.get("https://ntnu.blackboard.com/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_70_1")
            sleep(7)
            infoList=[]
            courses = driver.find_element_by_class_name("courseListing")
            elementList = courses.find_elements_by_tag_name("li")
            courseDescription = elementList[n].text
            elementList[n].click()
            driver.implicitly_wait(5)
	    
            courses = driver.find_elements_by_class_name("h-va-baseline")
	    driver.implicitly_wait(8)
	    driver.find_element_by_xpath('//*[@title="\xc3\x98vinger"]').click()
	    driver.find_element_by_id("courseMenu_link").click
            sleep(sleepTimer)
	    #driver.find_element_by_xpath('//*[@title="\xc3\x98vinger"]').click()
	    #driver.find_element_by_class_name("clickpuller")
           # sleep(sleepTimer)
	   # menuItem=driver.find_element_by_id("courseMenuPalette_contents")
	   # print menuItem.text
	   # ovingItem = menuItem.find_elements_by_tag_name("li")
	  #  for n in range(len(ovingItem)):
	 #       if(n==7):
	#	    print(ovingItem[n].text)
	#	    ovingItem[n].click()
            #driver.find_element_by_xpath('//*[@title="\xc3\x98vinger"]').click()
	   
            #time.sleep(10)
            excersises = driver.find_element_by_class_name("courseListing")
            singleExercises = excersises.find_elements_by_tag_name("li")
            for n in range(len(singleExercises)):
                assignmentsForACourse=[]
                assignmentsForACourse.append(courseDescription +"| " + singleExercises[n].text)
                allDeliveriesList.append(assignmentsForACourse)
        driver.quit()
        display.stop()
        return allDeliveriesList
    except:
        print "did not find any assignments for you on blackboard"
        driver.quit()
        display.stop()
        traceback.print_exc()
        return allDeliveriesList

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

def parceFromBlackBoardToDatabase(doubleScrapeListFromBB):
    returnList = []
    for deliveries in doubleScrapeListFromBB:
        deliveries = deliveries[0]
        course = deliveries.split("|")[0]
        try:
            deadLineDate = deliveries.split("Deadline")[1]
            returnList.append(course+"|"+deadLineDate)
        except:
            continue
    return returnList

#in ['TDT4145 Datamodellering og databasesystemer (2017 V\xc5R)| 26. Jan 23.59.',
def monthConverter(monthAsString):
    months=["Jan","Feb","Mar","Apr","Mai","Jun","Jul","Aug","Sept","Okt","Nov","Des"]
    returnVar = 0
    for n in range(len(months)):
        if months[n]==monthAsString:
            returnVar = n + 1 
            break
    if(returnVar==0):
        returnVar = "00" 
    return str(returnVar)

def convertTimeToRightFormate(timeString):
    temp=""
    for n in timeString:
        if(isNumber(n)):
            temp=temp+n
    return temp[0:2]+":"+temp[2:4]+":"+"00"

def inScrapeOutListWithCourseAndDeliveryDate(scrape):
    trimmedScrape = parceFromBlackBoardToDatabase(scrape)
    returnList=[]
    counter = 1
    for entries in trimmedScrape:
        tempList = []
        courseName = entries.split("(")[0]
        dateString = entries.split("|")[1]
        day = dateString.split()[0]
        daySplit=day.split(".")[0]
        tempList.append("Assignment " + str(counter))
        tempList.append(courseName)
        day = getDateOnRightFormat(daySplit)
        mounth = getDateOnRightFormat(monthConverter(dateString.split()[1]))
        year = entries.split("(")[1][0:4]
        tempList.append(year+"-"+mounth+"-"+day)
        counter +=1
        time = dateString.split(" ")[3]
        time = convertTimeToRightFormate(time)
        tempList.append(time)
        returnList.append(tempList)
    return returnList

def scrapeAndGetRawReadyForDatabase():
    scrape=scrapeBlackBoard(6)
    return inScrapeOutListWithCourseAndDeliveryDate(scrape)
print(scrapeAndGetRawReadyForDatabase())
