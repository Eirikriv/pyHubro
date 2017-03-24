from selenium import webdriver
import time
from pyvirtualdisplay import Display
from selenium import webdriver
from getpass import getpass

def scrapeItslearning():
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver=webdriver.Firefox()
    u_username=raw_input("NTNU username: ")
    u_password=getpass("NTNU password: ")
    driver.get('http://www.instabart.no/') 

    pressend=driver.find_element_by_class_name("itslearning")
    time.sleep(1)
    pressend.click()
 
    time.sleep(3)
    its=driver.find_element_by_id("username")
    time.sleep(1)
    its.send_keys(u_username) 

    passwd = driver.find_element_by_id("password")
    time.sleep(1)
    passwd.send_keys("u_password")


    loginbutton = driver.find_element_by_class_name("submit")
    time.sleep(1)
    loginbutton.click()
    #https://ntnu.itslearning.com/main.aspx?TextURL=Course%2fAllCourses.aspx
    time.sleep(4)
    #driver.get('https://ntnu.itslearning.com//main.aspx?CourseID=63699&ElementID=3248815&ElementType=512')
    #time.sleep(2)
    driver.get("https://ntnu.itslearning.com/DashboardMenu.aspx?LocationType=Hierarchy")
    time.sleep(4)
    driver.switch_to.frame(driver.find_element_by_name("mainmenu"))
    time.sleep(2) 
    #courses = driver.find_element_by_css_selector("li > .ccl-iconlink")
    #infolistelement on form : [title text, course]
    maininfoList=[]
    for n in range(0,len(driver.find_elements_by_class_name("h-va-baseline"))):
        infoList=[]
        driver.get("https://ntnu.itslearning.com/DashboardMenu.aspx?LocationType=Hierarchy")
        time.sleep(2)
        driver.switch_to.frame(driver.find_element_by_name("mainmenu"))
        time.sleep(2)
        courses = driver.find_elements_by_class_name("h-va-baseline")
        infoList.append(courses[n].text)
        courses[n].click()
        courseTitle=driver.find_element_by_class_name("treemenu-title")
        infoList.append(courseTitle.text)
        time.sleep(2)
        driver.switch_to.frame(driver.find_element_by_name("mainmenu"))
        time.sleep(2)
        assigmentInfo=driver.find_elements_by_class_name("h-mrb5")
        infoList.append(assigmentInfo[1].text)
        maininfoList.append(infoList)
    driver.quit()
    display.stop()
    return maininfoList

#Converts to the form: [AssimentDetails, CourseName, deadline date, deadline time]
def mounthConverter(mounthAsString):
    mounths=["januar","februar","mars","april","mai","juni","juli","august","september","oktober","november","desember"]
    returnVar = 0
    for n in range(len(mounths)-1):
        if mounths[n]==mounthAsString:
            returnVar = n + 1 
            break
    return str(returnVar)
    
def getDayOnRightFormat(day): #days can be 3. or 12., need to convert 3. to 03 and 12. to 12
    returnday = day[0:-1]
    if len(returnday)>=2:
        return returnday
    else:
        return "0"+returnday
def getMounthOnRightFormat(mounth):
    returnday = mounth
    if len(returnday)>=2:
        return returnday
    else:
        return "0"+returnday

def prepDeliveriesForDatabase(rawScrapeFromIts):
    returnList=[]
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
    day = getDayOnRightFormat(deadLineDetails[1])
    mounth=mounthConverter(deadLineDetails[2])
    mounth=getMounthOnRightFormat(mounth)

    year = deadLineDetails[3]
    dateString = year + "-" + mounth + "-" + day
    returnList.append(dateString)

    time = deadLineDetails[4]
    time = time + ":00"

    returnList.append(time)
    return returnList


def prepAllDeiveriesForDatabase(totalDeliveryList):
    returnList = []
    for deliveries in totalDeliveryList:
        returnList.append(prepDeliveriesForDatabase(deliveries))
    return returnList

def make():
    rawList = scrapeItslearning()
    print(rawList)
    readyForDataBase = prepAllDeiveriesForDatabase(rawList)
    return readyForDataBase
print(make())
