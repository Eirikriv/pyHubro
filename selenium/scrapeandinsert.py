# Start up an Xvfb display that has 0 window size
from pyvirtualdisplay import Display
#display.sendstop() #use this to close display after running 
# Load a Firefox selenium webdriver session
from selenium import webdriver
from getpass import getpass
from database import db
from database import Courses
from readCourseTimeTables import scrapeNtnuCourseWebsites
from readCourseTimeTables import readfile
import time

#import time to slow selenium down

#inserts a row into the Courses database
def insertIntoDatabase(studentID,CourseName,startTime,endTime,stardate,enddate,description,location,attachements):
    insertion = Courses(studentID,CourseName,startTime,endTime,stardate,enddate,description,location,attachements)
    db.session.add(insertion)
    db.session.commit()
    print("commitedToDB")


#Starts a virtual display, needed to run selenium on linux server

#Asks for username and password in console, then scrapes the itslearning page for the given username
#Returns the last course in the "Active" courselist
def scrapeItslearning():
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox()
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
    passwd.send_keys(u_password)


    loginbutton = driver.find_element_by_class_name("submit")
    time.sleep(1)
    loginbutton.click()

    time.sleep(4)

    driver.get('https://ntnu.itslearning.com/main.aspx?TextURL=Course%2fAllCourses.aspx')
    time.sleep(4)
    driver.switch_to.frame(driver.find_element_by_name("mainmenu"))
    time.sleep(4)
    courses = driver.find_elements_by_css_selector("td > .ccl-iconlink")

    listOfCourses = []

    for course in courses:
        listOfCourses.append(course.text)

    driver.quit()
    display.stop()
    return listOfCourses


def findCourseCode(courseCodeString):
    return courseCodeString.split(" ")[0]
#Scrapes, then inserts course into database with stuentid and courseid as hard-coded constants

def main():
    courses=scrapeItslearning()
    for course in courses:
        print(findCourseCode(course))
        try:        
            scrapeNtnuCourseWebsites(findCourseCode(course))
            tableToInsert=readfile()
            print(tableToInsert)
	    tableToInsert = tableToInsert[0]
            print tableToInsert
            insertIntoDatabase("01",course,tableToInsert[0],tableToInsert[1],tableToInsert[2],tableToInsert[3],tableToInsert[4],tableToInsert[5],tableToInsert[6])
            break
        except:
            continue       
main()
