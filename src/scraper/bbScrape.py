from selenium import webdriver
from scrapingSiteCredentials import *
import time
from pyvirtualdisplay import Display
import traceback
from selenium.webdriver.common.keys import Keys
def scrapeBlackBoard():
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver=webdriver.Firefox()

        driver.get('http://www.instabart.no/') 

        pressend=driver.find_element_by_id("blackboard")
        time.sleep(1)
        pressend.click()

        time.sleep(3)
        el = driver.find_element_by_id('org')
        for option in el.find_elements_by_tag_name('option'):
            if(option.text == 'NTNU'):
                option.click() 
                break
        pressSubmit=driver.find_element_by_id("submit")
        pressSubmit.click()
        time.sleep(2)
        its=driver.find_element_by_id("username")
        time.sleep(1)
        its.send_keys(unameBlackBoard) 

        passwd = driver.find_element_by_id("password")
        time.sleep(1)
        passwd.send_keys(passBlackBoard)


        loginbutton = driver.find_element_by_class_name("submit")
        loginbutton.click()
        time.sleep(10)
        courses = driver.find_element_by_class_name("courseListing")
        elementList = courses.find_elements_by_tag_name("li")
        allDeliveriesList = []
        for n in range(0,len(elementList)):
            
            driver.get("https://ntnu.blackboard.com/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_70_1")
            time.sleep(2)
            infoList=[]
            courses = driver.find_element_by_class_name("courseListing")
            elementList = courses.find_elements_by_tag_name("li")
            courseDescription = elementList[n].text
            elementList[n].click()
            time.sleep(2)
            courses = driver.find_elements_by_class_name("h-va-baseline")
            time.sleep(4)
	    elem=driver.find_element_by_xpath('//*[@title="Forelesninger"]')
	    elem.send_keys(Keys.TAB)
	    elem.click()
            excersises = driver.find_element_by_id("content_listContainer")
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
        traceback.print_exc()
        return None
    #finally:
        #driver.quit()
        #display.close()

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
    scrape=scrapeBlackBoard()
    return inScrapeOutListWithCourseAndDeliveryDate(scrape)

scrapeAndGetRawReadyForDatabase()
