#Used to create daily reports and convert into PDF and email
#3June2015 - So far have creating PDF Report from SQL database.
#Need to:
#   change SQL read to be day before when have live data
#   send PDf report as email


import time
from reportlab.pdfgen import canvas
import datetime
import psycopg2
from reportlab.lib.colors import red, green, blue, orange, purple
from gmail_Module import *
from error_Logging import logWrite

def getData():

    con = psycopg2.connect("host=<host ip address> dbname=<database_name> user=<username> password=<password>")#connect to dB
    cur = con.cursor()
    dayBefore = time.strftime("%Y-%m-%d",time.localtime((time.time() - 86400)))
    cur.execute("select * from data_history where date_ = '{}' order by id Asc".format(dayBefore))
    sqlResult = cur.fetchall()
    cur.close()
    con.close()

    dataMemory1 = []
    dataMemory2 = []
    dataMemoryAver = []
    timeMemory = []

    counterA = 0
    try:
        while counterA < (len(sqlResult)):#Until EOF read
            timeDataRaw = sqlResult[counterA][2];#print timeDataRaw
            temp1DataRaw = sqlResult[counterA][3];#print tempDataRaw
            temp2DataRaw = sqlResult[counterA][4];#print tempDataRaw
            averageDataRaw = sqlResult[counterA][5];#print tempDataRaw
            temp1DataScaled = int(float(temp1DataRaw) * 20) + 100
            temp2DataScaled = int(float(temp2DataRaw) * 20) + 100
            averageDataScaled = int(float(averageDataRaw) * 20) + 100
            timeDataHr = int(timeDataRaw[0:2]);#print timeDataHr
            timeDatamin = int(timeDataRaw[3:5]);#print timeDatamin
            timeDataminScaled = float((timeDataHr * 60) + timeDatamin)/2
            timeMemory.append(timeDataminScaled)
            dataMemory1.append(temp1DataScaled)
            dataMemory2.append(temp2DataScaled)
            dataMemoryAver.append(averageDataScaled)
            counterA += 1
        return timeMemory, dataMemory1, dataMemory2, dataMemoryAver
    except ValueError:
        logWrite("Error: create_Report module error")

def GraphData(c,xdata,y1data,y2data,y3data):

#Graph Sensor 1 Temperatures
    counterB = 0
    while counterB < (len(xdata)) - 1:
        c.setStrokeColor(red)
        c.line((xdata[counterB]) + 250,(y1data[counterB] + 400),(xdata[counterB + 1]) + 250, (y1data[counterB + 1] + 400))
        counterB += 1
#Graph Sensor 2 Temperatures
    counterC = 0
    while counterC < (len(xdata)) - 1:
        c.setStrokeColor(purple)
        c.line((xdata[counterC]) + 250,(y2data[counterC] + 400),(xdata[counterC + 1]) + 250, (y2data[counterC + 1] + 400))
        counterC += 1
#Graph Average of Sensor 1 and Sensor 2
    counterD = 0
    while counterD < (len(xdata)) - 1:
        c.setStrokeColor(orange)
        c.line((xdata[counterD]) + 250,(y3data[counterD] + 400),(xdata[counterD + 1]) + 250, (y3data[counterD + 1] + 400))
        counterD += 1

#Calculate, graph and display Minimum Temps
    c.setStrokeColor(blue)
    minTemp = str(((min(y1data)) - 100) / 20) + (unicode((chr(176)),'latin-1')) + "C"
    c.line(250,(min(y1data)) + 400,(max(xdata)) + 250, (min(y1data)) + 400)#Min Temp Line
    c.drawString(max(xdata) + 300, (min(y1data)) + 390,text=minTemp)
    minimumIndex = y1data.index(min(y1data))
    minimumTimeRaw = xdata[minimumIndex]
    minimumTimeSecs = (minimumTimeRaw*2)*60
    minimumTemp = str((float(min(y1data)-100))/20) + " " + ((unicode((chr(176)),'latin-1')) + "C")
    minimumTempTime = str(datetime.timedelta(seconds=minimumTimeSecs))
    c.drawString(200,1250,text="Minimum Temperature")
    c.drawString(450,1250,text=": " + minimumTemp)
    c.drawString(620,1250,text="Minimum Temp Time")
    c.drawString(870,1250,text=": {} hrs".format(minimumTempTime))

#Calculate, graph and display Maximum Temps
    c.setStrokeColor(green)
    maxTemp = str(((max(y2data)) - 100) / 20) + (unicode((chr(176)),'latin-1')) + "C"
    c.line(250,(max(y2data)) + 400,(max(xdata)) + 250, (max(y2data)) + 400)#Max Temp Line
    c.drawString(max(xdata) + 300, (max(y2data)) + 395,text=maxTemp)
    maximumIndex = y2data.index(max(y2data))
    maximumTimeRaw = xdata[maximumIndex]
    maximumTimeSecs = (maximumTimeRaw*2)*60
    maximumTemp = str((float(max(y2data)-100))/20) + " " + ((unicode((chr(176)),'latin-1')) + "C")
    maximumTempTime = str(datetime.timedelta(seconds=maximumTimeSecs))
    c.drawString(200,1290,text="Maximum Temperature")
    c.drawString(450,1290,text=": " + maximumTemp)
    c.drawString(620,1290,text="Maximum Temp Time")
    c.drawString(870,1290,text=": {} hrs".format(maximumTempTime))

def GraphFrame(c,xdata):
    #Report Header
    c.setFont("Times-Roman",60)
    c.drawString(375,1520,text="The Brewery Daily")
    c.drawString(360,1450,text="Temperature Report")
    #Report Footer
    c.setFont("Times-Roman",18)
    footerDate = time.strftime("%b %d %Y",time.localtime((time.time())))
    c.drawString(950,80,text=footerDate)
    footerName = "BreweryReport_{}.pdf".format((time.strftime("%Y%m%d",time.localtime((time.time())))))
    c.drawString(50,80,text=footerName)
    #Report Frame
    c.setFont("Times-Roman",24)
    c.line(250,400,(max(xdata) + 250), 400)
    c.line(250,1200,(max(xdata) + 250), 1200)
    c.line(250,400,250,1200)
    c.line((max(xdata) + 250),400,(max(xdata) + 250), 1200)
    c.drawString(150,500,text="0" + (unicode((chr(176)),'latin-1')) + "C")
    c.drawString(150,600,text="5" + (unicode((chr(176)),'latin-1')) + "C")
    c.drawString(150,700,text="10" + (unicode((chr(176)),'latin-1')) + "C")
    c.drawString(150,800,text="15" + (unicode((chr(176)),'latin-1')) + "C")
    c.drawString(150,900,text="20" + (unicode((chr(176)),'latin-1')) + "C")
    c.drawString(150,1000,text="25" + (unicode((chr(176)),'latin-1')) + "C")
    c.drawString(150,1100,text="30" + (unicode((chr(176)),'latin-1')) + "C")
    counterE = 0
    increments = (float(max(xdata)) / 24)
    while counterE <= 24:
        c.line(250 + (increments * counterE), 400, 250 + (increments * counterE), 380)
        if counterE == 0:
            c.drawString(245 + (increments * counterE), 335,text= "0")
            c.line(250 + (increments * counterE), 400, 250 + (increments * counterE), 360)
        if counterE == 6:
            c.drawString(232 + (increments * counterE), 335,text= "6:00")
            c.line(250 + (increments * counterE), 400, 250 + (increments * counterE), 360)
        if counterE == 12:
            c.drawString(223 + (increments * counterE), 335,text= "12:00")
            c.line(250 + (increments * counterE), 400, 250 + (increments * counterE), 360)
        if counterE == 18:
            c.drawString(223 + (increments * counterE), 335,text= "18:00")
            c.line(250 + (increments * counterE), 400, 250 + (increments * counterE), 360)
        if counterE == 24:
            c.drawString(245 + (increments * counterE), 335,text= "0")
            c.line(250 + (increments * counterE), 400, 250 + (increments * counterE), 360)
        counterE += 1
    c.setStrokeColor(purple)
    c.line(250,275,350,275)
    c.drawString(260,250,text= "Sensor 1")
    c.setStrokeColor(red)
    c.line(562,275,662,275)
    c.drawString(572,250,text= "Sensor 2")
    c.setStrokeColor(orange)
    c.line(862,275,962,275)
    c.drawString(872,250,text= "Average")


def send_Report(configuration):
    reportFileName = "BreweryReport_{}.pdf".format((time.strftime("%Y%m%d",time.localtime((time.time() - 86400)))))
    c = canvas.Canvas(reportFileName)
    c.scale(0.5,0.5)
    dataList = getData()
    GraphFrame(c,dataList[0])
    GraphData(c,dataList[0],dataList[1],dataList[2],dataList[3])
    c.showPage()
    c.save()
    time.sleep(3)
    fileLocation = configuration[9][2]
    emailAddress = configuration[7][2]
    DailyReportEmail(fileLocation,reportFileName,emailAddress)
