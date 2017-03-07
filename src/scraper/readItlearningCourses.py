# Start up an Xvfb display that has 0 window size
from pyvirtualdisplay import Display
#display.sendstop() #use this to close display after running 
# Load a Firefox selenium webdriver session
from selenium import webdriver
from readItlearningCourses.py import scrapeNtnuCourseWebsites
from scrapingSiteCredentials import *
import time
import traceback
def getUsername(): #get NTNU Feide username from user
    u_username=unameItslearning
    return u_username

def getUserPassword(): #get NTNU Feide password from user
    u_password=passItslearning
    return u_password

def sleep(sleepTimer): #sleep selenium so pages can load before next action is taken
    time.sleep(sleepTimer)
    return 


#Starts a virtual display, needed to run selenium on linux server

#Asks for username and password in console, then scrapes the itslearning page for the given username
#Returns the last course in the "Active" courselist
def scrapeItslearning(sleepTimer):
    try:  
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = webdriver.Firefox()
        u_username=getUsername()
        u_password=getUserPassword()
        driver.get('http://www.instabart.no/') 
        pressend=driver.find_element_by_class_name("itslearning")
        sleep(sleepTimer)
        pressend.click()
        sleep(sleepTimer)
        its=driver.find_element_by_id("username")
        sleep(sleepTimer)
        its.send_keys(u_username) 
        passwd = driver.find_element_by_id("password")
        sleep(sleepTimer)
        passwd.send_keys(u_password)
        loginbutton = driver.find_element_by_class_name("submit")
        sleep(sleepTimer)
        loginbutton.click()
        sleep(sleepTimer)
        driver.get('https://ntnu.itslearning.com/main.aspx?TextURL=Course%2fAllCourses.aspx')
        sleep(sleepTimer)
        driver.switch_to.frame(driver.find_element_by_name("mainmenu"))
        sleep(sleepTimer)
        courses = driver.find_elements_by_css_selector("td > .ccl-iconlink")
        listOfCourses = []
        for course in courses:
            listOfCourses.append(course.text)
        driver.quit()
        display.stop()
        return listOfCourses
    except:
        print "did not find any courses for you on itslearning"
        driver.quit()
        display.stop()
        traceback.print_exc()
        return None


def findCourseCode(courseCodeString):
    return courseCodeString.split(" ")[0]
#Scrapes itslearning

def main():
    courses=scrapeItslearning(3)
    try:
        for course in courses:
            print(findCourseCode(course))
            try:        
                scrapeNtnuCourseWebsites(findCourseCode(course))
                #TODO
            except:
                traceback.print_exc()
                print "no times found on coursesite"
                continue   
    except:
        traceback.print_exc()
        print "error"

