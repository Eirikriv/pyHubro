from pyvirtualdisplay import Display
from selenium import webdriver
import time
import datetime
def convertweekAndDayToDate(dayAsString,weekNrAsString,yearAsString):
    days = ["Mandag","Tirsdag","Onsdag","Torsdag","Fredag"]
    d = yearAsString + "-W" + weekNrAsString 
    r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    r= str(r)
    return r[0:10]


def readfile():
    filee = open("courseContent.txt","r")
    array=[]
    for line in filee:
        line = line.replace("\n","")
        array.append(line)  
    del array[0]
    mainReturnArray=[]
    for elements in array: #converts the incoming string to the formate below 
        returnArray=[]
        elements=elements+" "#WARNING ONLY NORWEGIAN PARCING WORKS DUE TO KEYWORDSPESSIFIC PARCING
        spittedList=[]
        tempWord=""
        for letters in elements:
            if(letters==" "):
                spittedList.append(tempWord)
                tempWord=""
            else:
                tempWord = tempWord + letters
        returnArray.append(spittedList[1])
        returnArray.append(spittedList[3])
        startdate = ""
        startdate = convertweekAndDayToDate(spittedList[0],"9","2017")
        startdate = str(startdate) + "T" + str(spittedList[1] + ":00")
        returnArray.append(startdate)
        enddate = ""
        enddate = convertweekAndDayToDate(spittedList[0],"9","2017")
        enddate = str(enddate) + "T" + str(spittedList[3] + ":00")
        returnArray.append(enddate)
        returnArray.append(spittedList[5])
        returnArray.append(spittedList[-1])
        returnArray.append("None")
        mainReturnArray.append(returnArray)
    return mainReturnArray
print(readfile())
#All events will be saved in the following way: 
#[starttime,endtime,startdate,enddate,description,where,attachments]
#saved within a list on the form:
#[event1,event2,event3]


def scrapeNtnuCourseWebsites(courseCode): #eks TIO4110, gives a long string of courses and times, needs to be modified
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
    text_file = open("courseContent.txt","w")
    text_file.write(unicode_string)
    text_file.close()
    
#startdisplay()
#scrapeNtnuCourseWebsites("TDT4140")
#print(readfile())
