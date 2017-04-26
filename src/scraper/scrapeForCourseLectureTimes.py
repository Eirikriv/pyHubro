from pyvirtualdisplay import Display
from selenium import webdriver
import traceback
import time
import datetime

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def convertweekAndDayToDate(dayAsString,weekNrAsString,yearAsString):
    days = ["Mandag","Tirsdag","Onsdag","Torsdag","Fredag"]
    counter =0
    for n in range(len(days)):
        if(dayAsString==days[n]):
            counter = n+1

    d = yearAsString + "-W" + weekNrAsString 
    r = datetime.datetime.strptime(d + "-"+str(counter), "%Y-W%W-%w")
    r= str(r)
    return r[0:10]

#Takes in a scrape and converts it to databasefriendly fields, NOT DUBPLICATE, this is for coursescraping, the other on in scraper/loginAndScrapeBlackBoard.py is for BlackBoard scrapes
def readCourseReturnAllLectureExersiseEvents(scrapeFromCourseSite, coursecode, year):
    courseScrape=scrapeFromCourseSite
    courseSemesterTimeTable=[]
    for elements in courseScrape: 
        tempList=elements.split()
        day=tempList[0]
        startTime = "T" + tempList[1] + ":00"
        endTime = "T"+ tempList[3] + ":00"
        description = tempList[5]
        where = tempList[-1]
        weeks = tempList[4]
        weeks = weeks.split("-")
        foreloopStart = weeks[0]
        foreloopEnd = weeks[1].split(",")[0]
        additionalWeeks = weeks[1].split(",")[1]
        weeklyevents=[]
        
        for n in range(int(foreloopStart),int(foreloopEnd)+1):
            tempListTwo=[]
            startDateTime = convertweekAndDayToDate(day,str(n),year)+startTime
            endDateTime = convertweekAndDayToDate(day,str(n),year)+endTime
            tempListTwo.append(coursecode)
            tempListTwo.append(startDateTime)
            tempListTwo.append(endDateTime)
            tempListTwo.append(description)
            tempListTwo.append(where)
            weeklyevents.append(tempListTwo)
        courseSemesterTimeTable.append(weeklyevents)
    return courseSemesterTimeTable



def scrapeNtnuCourseWebsites(courseCode): #Scrapes for courses lectures 
    returnList=""
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
    webpage = "https://www.ntnu.no/studier/emner/"+courseCode+"#tab=timeplan"
    driver.get(webpage)
    time.sleep(1)
    courseTable=driver.find_element_by_class_name("wrap")    
    text=courseTable.text
    driver.quit()
    # break into lines and remove leading and trailing space on each	
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)  
    unicode_string = text.encode('utf-8')
    returnList = unicode_string.splitlines()
    del returnList[0]
    display.stop()
    return returnList , courseCode





