#Main alarm monitor and report raising engine.
# -*- coding: utf-8 -*-

import time
from gmail_Module import *
import psycopg2
import thread
import create_Report
from error_Logging import logWrite
global temp_low, temp_high, reset_alarm, LES, HES

def Send_Alarm_Email(subjectText,bodyText,configuration):
    emailAddress = configuration[7][2]
    emailText(subjectText,bodyText,emailAddress)

def HighHigh(cD,configuration):
    subjectText = "{}°C  The Mouldystalk Brewery - High High Alarm".format(cD[0][5])
    bodyText = "Please investigate a High Temperature Alarm\n" \
        " - Current Temperature is {}°C".format(cD[0][5])
    Send_Alarm_Email(subjectText,bodyText, configuration)
def LowLow(cD,configuration):
    subjectText = "{}°C  The Mouldystalk Brewery - Low Low Alarm".format(cD[0][5])
    bodyText = "Please investigate a Low Temperature Alarm\n" \
        " - Current Temperature is {}°C ".format(cD[0][5])
    Send_Alarm_Email(subjectText,bodyText, configuration)
def AlarmReset(cD,configuration):
    subjectText = "{}°C  The Mouldystalk Brewery - Alarm Reset".format(cD[0][5])
    bodyText = "The Temperature Alarm has been Reset\n" \
        " - Current Temperature is {}°C ".format(cD[0][5])
    Send_Alarm_Email(subjectText,bodyText, configuration)
def temp_alarm(curDat, configuration):
    global temp_low, temp_high, reset_alarm, LES, HES
    if curDat[0][7] == True and temp_low < 10:
        temp_low += 1
        time.sleep(1)
        #print"Tick Low"
        if temp_low > 9 and LES == False:
            LowLow(curDat,configuration)
            logWrite("Alarm: Low Low Alarm email sent")
            #print "low temp email to send"
            LES = True
    if curDat[0][8] == True and temp_high < 10:
        temp_high += 1
        time.sleep(1)
        #print"Tick High"
        if temp_high > 9 and HES == False:
            HighHigh(curDat,configuration)
            logWrite("Alarm: High High Alarm email sent")
            #print "high temp email to send"
            HES = True
    if (curDat[0][7] == False and temp_low > 9 and LES == True) or (curDat[0][8] == False and temp_high > 9 and HES == True):
        #print "reset alarm email"
        reset_alarm += 1
        time.sleep(1)
        if reset_alarm > 10:
            #print "send reset alarm email"
            logWrite("Alarm: Temperature Alarm Reset email sent")
            temp_low = 0
            LES = False
            temp_high = 0
            HES = False
            reset_alarm = 0
            AlarmReset(curDat,configuration)


def alarm_Monitor_cycle(configuration):
    global temp_low, temp_high, reset_alarm, LES, HES

    counterA = 0
    temp_low = 0
    temp_high = 0
    reset_alarm = 0
    LES = False
    HES = False
    SER = False
    while counterA < 1000:
        curTime = int(time.strftime("%H%M",time.localtime((time.time()))))
        #print curTime
        #print configuration[8][2]
        if curTime == int(configuration[8][2]) and SER == False:
            SER = True
            #print "Send Email Report"
            thread.start_new_thread(create_Report.send_Report,(configuration,),)
        if curTime == int(configuration[8][2]) + 1 and SER == True:
            SER = False
            #print "Reset Email report counter"
        con = psycopg2.connect("host=<host ip address> dbname=<database_name> user=<username> password=<password>")
        cur = con.cursor()
        cur.execute("SELECT * FROM current_data")
        curDat = cur.fetchall()
        temp_alarm(curDat, configuration)
        cur.close()
        con.close()
        time.sleep(5)

