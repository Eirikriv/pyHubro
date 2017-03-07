import time
from pyvirtualdisplay import Display
from selenium import webdriver
from getpass import getpass
from scrapingSiteCredentials import *
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

def loginAndGoToItslearningMainPage(sleepTimer):
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver=webdriver.Firefox()
    driver.get('http://www.instabart.no/') 
    itslearningButton=driver.find_element_by_class_name("itslearning")
    sleep(sleepTimer)
    itslearningButton.click() #now try to login to itslearning
    sleep(sleepTimer)
    loggedIn = False
    while(not loggedIn):
        try:
            username = getUsername()
            password = getUserPassword()
            its=driver.find_element_by_id("username")
            sleep(sleepTimer)
            its.send_keys(username)
            passwd = driver.find_element_by_id("password")
            sleep(sleepTimer)
            passwd.send_keys(password)
            loginbutton = driver.find_element_by_class_name("submit")
            sleep(sleepTimer)
            loginbutton.click()
            loggedIn=True
            break
        except:
            traceback.print_exc()
            print "Wrong username or password, please try again and use the login you would use for itslearning (Feide)"
    sleep(sleepTimer)
    driver.get("https://ntnu.itslearning.com/DashboardMenu.aspx?LocationType=Hierarchy")
    time.sleep(sleepTimer)
    driver.switch_to.frame(driver.find_element_by_name("mainmenu"))
    time.sleep(sleepTimer) 
    maininfoList=[]
    try:
        for n in range(0,len(driver.find_elements_by_class_name("h-va-baseline"))):
            infoList=[]
            driver.get("https://ntnu.itslearning.com/DashboardMenu.aspx?LocationType=Hierarchy")
            sleep(sleepTimer)
            driver.switch_to.frame(driver.find_element_by_name("mainmenu"))
            sleep(sleepTimer)
            courses = driver.find_elements_by_class_name("h-va-baseline")
            infoList.append(courses[n].text)
            courses[n].click()
	    sleep(sleepTimer)
            courseTitle=driver.find_element_by_class_name("treemenu-title")
            infoList.append(courseTitle.text)
            sleep(sleepTimer)
            driver.switch_to.frame(driver.find_element_by_name("mainmenu"))
            sleep(sleepTimer)
            assigmentInfo=driver.find_elements_by_class_name("h-mrb5")
            infoList.append(assigmentInfo[1].text)
            maininfoList.append(infoList)
    except: 
        print ("Could not find any assigments for you on itslearning")
        traceback.print_exc()
    
    driver.quit()
    display.stop()
    return maininfoList
print(loginAndGoToItslearningMainPage(4))
