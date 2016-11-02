
from Tkinter import *
import config_Settings
import killProgram
import time
import thread
import psycopg2
import gc
import display_Report
from error_Logging import logWrite

class mainWindow:
    def __init__(self):
        self.WriteReg = {}
        self.degreesC = u"\N{DEGREE SIGN}" + "C"
    def displayReportWindow(self):
        report = display_Report.reportWindow()
        report.dispData()
    def configMenu(self):
        openConfig = config_Settings.configWindow()
        openConfig.configGui()
    def shutdownMenu(self):
        logWrite("System: Shutdown BreweryHMI Program")
        ShutdownPopup = killProgram.endProgram()
        ShutdownPopup.exitPopup()
    def upButton(self,v,i):
        v += 0.1
        self.WriteReg[i] = v
    def downButton(self,v,i):
        v -= 0.1
        self.WriteReg[i] = v
    def loadCurrentData(self):
        conLCD = psycopg2.connect("host=<host ip address> dbname=<database_name> user=<username> password=<password>")
        cur = conLCD.cursor()
        query1 = cur.execute("SELECT * FROM current_data")
        RawResult = cur.fetchall()
        cur.close()
        conLCD.close()
        return RawResult
    def loadVariables(self):
        conLV = psycopg2.connect("host=<host ip address> dbname=<database_name> user=<username> password=<password>")
        cur = conLV.cursor()
        query1 = cur.execute("SELECT count(*) FROM threshold_variables")
        RawResult1 = cur.fetchall()
        result1 = RawResult1[0][0]
        b = 1
        while b < result1 + 1:
            query2 = cur.execute("SELECT register_value FROM threshold_variables WHERE id = %s" %(b))
            RawResult2 = cur.fetchall()
            result2 = RawResult2[0][0]
            self.WriteReg[b-1] = float(result2)
            b += 1
        cur.close()
        conLV.close()
    def saveVariables(self):
        convar = psycopg2.connect("host=<host ip address> dbname=<database_name> user=<username> password=<password>")
        curvar = convar.cursor()
        lenghtWriteReg = (len(self.WriteReg))
        SVCount = 0;
        while SVCount < lenghtWriteReg:
            curvar.execute("UPDATE threshold_variables SET register_value = %s WHERE id = %s",((round((self.WriteReg[SVCount]),2)),SVCount+1))
            SVCount += 1
            convar.commit()
        curvar.close()
        convar.close()
    def mainGui(self,configuration):
        window = Tk()
        gc.enable()
        self.loadVariables()#Loads alarm and Fermination thresholds variables from SQL
        window.geometry("1020x620+100+10")
        window.title("The Brewery HMI - Main Page")
        mainbox = Canvas(window, width=1010, height=610, bg = '#DCDCDC')
        mainbox.pack()
        #FermTempThresholds
        FermArea = mainbox.create_rectangle(15, 15, 315, 300, fill="white")
        #MaxFerm
        FermMaxTitle = mainbox.create_text(30, 50, font=("Arial", 14, "bold"), anchor="w", fill='black', text="Max Fermentation\nTemperature Threshold")
        self.FermMaxTemp = mainbox.create_text(150,115, font=("Arial", 24, "bold"), anchor="w", fill='black', text=self.WriteReg[3])
        max_upBut = Button(window, font=("Arial", 12, "bold"), text="^", command=lambda: self.upButton(self.WriteReg[3],3))
        max_dnBut = Button(window, font=("Arial", 12, "bold"), text="v", command=lambda: self.downButton(self.WriteReg[3],3))
        FermMaxUpBut = mainbox.create_window(50,100,anchor="w",window=max_upBut)
        FermMaxDnBut = mainbox.create_window(50,130,anchor="w",window=max_dnBut)
        #MinFerm
        FermMinTitle = mainbox.create_text(30, 180, font=("Arial", 14, "bold"), anchor="w", fill = 'black', text ="Min Fermentation\nTemperature Threshold")
        self.FermMinTemp = mainbox.create_text(150,245, font=("Arial", 24, "bold"), anchor="w", fill='black', text=self.WriteReg[0])
        min_upBut = Button(window, font=("Arial", 12, "bold"), text="^", command=lambda: self.upButton(self.WriteReg[0],0))
        min_dnBut = Button(window, font=("Arial", 12, "bold"), text="v", command=lambda: self.downButton(self.WriteReg[0],0))
        FermMinUpBut = mainbox.create_window(50,230,anchor="w",window=min_upBut)
        FermMinDnBut = mainbox.create_window(50,260,anchor="w",window=min_dnBut)
        #AlarmTempThresholds
        AlarmArea = mainbox.create_rectangle(330, 15, 645, 300, fill="white")
        #HHFerm
        FermHHTitle = mainbox.create_text(345, 50, font=("Arial", 14, "bold"), anchor="w", fill = 'black', text ="High High Temperature\nAlarm Threshold")
        self.FermhhTemp = mainbox.create_text(465,115, font=("Arial", 24, "bold"), anchor="w", fill='black', text=self.WriteReg[2])
        hh_upBut = Button(window, font=("Arial", 12, "bold"), text="^", command=lambda: self.upButton(self.WriteReg[2],2))
        hh_dnBut = Button(window, font=("Arial", 12, "bold"), text="v", command=lambda: self.downButton(self.WriteReg[2],2))
        FermHHUpBut = mainbox.create_window(365,100,anchor="w",window=hh_upBut)
        FermHHDnBut = mainbox.create_window(365,130,anchor="w",window=hh_dnBut)
        #LLFerm
        FermLLTitle = mainbox.create_text(345, 180, font=("Arial", 14, "bold"), anchor="w", fill = 'black', text ="Low Low Temperature\nAlarm Threshold")
        self.FermllTemp = mainbox.create_text(465,245, font=("Arial", 24, "bold"), anchor="w", fill='black', text=self.WriteReg[1])
        ll_upBut = Button(window, font=("Arial", 12, "bold"), text="^", command=lambda: self.upButton(self.WriteReg[1],1))
        ll_dnBut = Button(window, font=("Arial", 12, "bold"), text="v", command=lambda: self.downButton(self.WriteReg[1],1))
        FermLLUpBut = mainbox.create_window(365,230,anchor="w",window=ll_upBut)
        FermLLDnBut = mainbox.create_window(365,260,anchor="w",window=ll_dnBut)
        #Sensor Temperatures
        SensorTempArea = mainbox.create_rectangle(15, 315, 315, 600, fill="white")
        Sens1Title = mainbox.create_text(30, 350, font=("Arial", 14, "bold"), anchor="w", fill = 'black', text ="Sensor 1\nTemperature: ")
        self.Sens1Temp = mainbox.create_text(180, 345, font=("Arial", 24, "bold"), anchor="w", fill='black', text="0")
        Sens2Title = mainbox.create_text(30, 450, font=("Arial", 14, "bold"), anchor="w", fill = 'black', text ="Sensor 2\nTemperature: ")
        self.Sens2Temp = mainbox.create_text(180, 445, font=("Arial", 24, "bold"), anchor="w", fill='black', text="0")
        AverTitle = mainbox.create_text(30, 550, font=("Arial", 14, "bold"), anchor="w", fill = 'black', text ="Average\nTemperature: ")
        self.AverTemp = mainbox.create_text(180, 545, font=("Arial", 24, "bold"), anchor="w", fill='black', text="0")
        #Misc
        dispRepBut = Button(window, text="Display Log", width=15, height=1,command=lambda: self.displayReportWindow())
        configBut = Button(window, text="Config / Settings", width=15, height=1, command=lambda: self.configMenu())
        shutBut = Button(window, text="Shutdown / Exit", width=15, height=1, command=lambda: self.shutdownMenu())
        DisplayReportBut = mainbox.create_window(850,525,anchor="w",window=dispRepBut)
        configMenuBut = mainbox.create_window(850,555,anchor="w",window=configBut)
        shutDownBut = mainbox.create_window(850,585,anchor="w",window=shutBut)
        #Indicators
        indArea = mainbox.create_rectangle(660,15,1000,300, fill='white')
        indAreaTitle = mainbox.create_text(675,50, font=("Arial", 14, "bold"), anchor="w", fill = 'black', text="Indicator Panel")
        self.k1 = mainbox.create_oval(710, 85, 710 + 15, 100, fill = "black")
        self.l1 = mainbox.create_text(710 + 60,90,anchor="w",text = "Low Low Temp Alarm")
        self.k2 = mainbox.create_oval(710, 125, 710 + 15, 140, fill = "black")
        self.l2 = mainbox.create_text(710 + 60,130,anchor="w",text = "High High Temp Alarm")
        self.k3 = mainbox.create_oval(710, 165, 710 + 15, 180, fill = "grey")
        self.l3 = mainbox.create_text(710 + 60,170,anchor="w",text = "Set Heater On")
        self.k4 = mainbox.create_oval(710, 205, 710 + 15, 220, fill = "grey")
        self.l4 = mainbox.create_text(710 + 60,210,anchor="w",text = "Set Chiller On")
        self.k5 = mainbox.create_oval(710, 245, 710 + 15, 260, fill = "black")
        self.l5 = mainbox.create_text(710 + 60,250,anchor="w",text = "Fridge Running")
        thread.start_new_thread(self.guiRefresh,(mainbox,),)
        window.mainloop()

    def guiRefresh(self,mainbox):
        time.sleep(0.2)
        valueA = 0
        while valueA < 10:
            curData = self.loadCurrentData()
            mainbox.delete(self.FermMaxTemp,self.FermMinTemp,self.FermhhTemp,self.FermllTemp)
            mainbox.delete(self.k1,self.k2,self.k5)
            mainbox.delete(self.Sens1Temp,self.Sens2Temp,self.AverTemp)
            self.FermMaxTemp = mainbox.create_text(150,115, font=("Arial", 24, "bold"), anchor="w", fill='black', text="{} ".format(float(self.WriteReg[3])) + self.degreesC)
            self.FermMinTemp = mainbox.create_text(150,245, font=("Arial", 24, "bold"), anchor="w", fill='black', text="{} ".format(float(self.WriteReg[0])) + self.degreesC)
            self.FermhhTemp = mainbox.create_text(465,115, font=("Arial", 24, "bold"), anchor="w", fill='black', text="{} ".format(float(self.WriteReg[2])) + self.degreesC)
            self.FermllTemp = mainbox.create_text(465,245, font=("Arial", 24, "bold"), anchor="w", fill='black', text="{} ".format(float(self.WriteReg[1])) + self.degreesC)
            self.Sens1Temp = mainbox.create_text(180, 345, font=("Arial", 24, "bold"), anchor="w", fill='black', text="{} ".format(float(curData[0][3])) + self.degreesC)
            self.Sens2Temp = mainbox.create_text(180, 445, font=("Arial", 24, "bold"), anchor="w", fill='black', text="{} ".format(float(curData[0][4])) + self.degreesC)
            self.AverTemp = mainbox.create_text(180, 545, font=("Arial", 24, "bold"), anchor="w", fill='black', text="{} ".format(float(curData[0][5])) + self.degreesC)
            if curData[0][6] == True:
                self.k5 = mainbox.create_oval(710, 245, 710 + 15, 260, fill = "green")
            else:
                if curData[0][6] == False:
                    self.k5 = mainbox.create_oval(710, 245, 710 + 15, 260, fill = "black")
            if curData[0][7] == True:
                self.k1 = mainbox.create_oval(710, 85, 710 + 15, 100, fill = "red")
            else:
                if curData[0][7] == False:
                    self.k1 = mainbox.create_oval(710, 85, 710 + 15, 100, fill = "black")
            if curData[0][8] == True:
                self.k2 = mainbox.create_oval(710, 125, 710 + 15, 140, fill = "red")
            else:
                if curData[0][8] == False:
                    self.k2 = mainbox.create_oval(710, 125, 710 + 15, 140, fill = "black")
            self.saveVariables()#Stores alarm and Fermination thresholds variables back to SQL
            gc.collect()
            time.sleep(1)



