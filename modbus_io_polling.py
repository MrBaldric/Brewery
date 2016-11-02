#Core I/O modbus device polling engine
#io_Pollingv2  29Oct2016
#  placed whole of modbus_Polling_cycle in a "while True:" loop to enable auto fix after comms failure.
#added pollErrors and pollOk variables to put debounce for error and Ok status of 10 events before changing state
import time
import pymodbus
import psycopg2
from error_Logging import logWrite
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus import exceptions
from gmail_Module import *
readHRRegs = {}; readFromCoils = {}; readFromDiscrete_Inputs = {}; numberRegs = 24; numberCoils = 16; numberDiscreteInputs = 8

def Send_Alarm_Email(subjectText,bodyText,configuration):
    emailAddress = configuration[7][2]
    emailText(subjectText,bodyText,emailAddress)

def modbus_Polling_cycle(configuration):
    pollError = 0
    counterA = 0
    pollOk = 0
    while True:
        try:
            client = ModbusClient(configuration[0][2])
            while counterA < 1000:
                ############################################################
                ########READ HOLDING REGISTERS##############################
                ############################################################
                holdingRegResult = client.read_holding_registers(int(configuration[4][2]), numberRegs)
                time.sleep(0.1)
                rr = 0
                while rr < numberRegs:
                    readHRRegs[rr] =round(((float(150)/410)/10) * int(holdingRegResult.getRegister(rr)),2)
                    if readHRRegs[rr] < 0:
                        readHRRegs[rr] = 0
                    rr += 1
                time.sleep(0.1)
                ############################################################
                ########READ MODBUS COILS###################################
                ############################################################
                readCoilResult = client.read_coils(int(configuration[3][2]), numberCoils)
                time.sleep(0.1)
                rb = 0
                while rb < numberCoils:
                    readFromCoils[rb] = readCoilResult.bits[rb]
                    rb += 1
                time.sleep(0.1)
                ############################################################
                ########READ DISCRETE INPUTS###################################
                ############################################################
                discreteInputsResult = client.read_discrete_inputs(int(configuration[6][2]), numberDiscreteInputs)
                time.sleep(0.1)
                di = 0
                while di < numberDiscreteInputs:
                    readFromDiscrete_Inputs[di] = discreteInputsResult.bits[di]
                    di += 1
                time.sleep(0.1)
                ############################################################
                ########SQL DATABASE WRITTING###############################
                ############################################################
                date1 = time.strftime("%Y-%m-%d")
                time1 = time.strftime("%H:%M:%S")
                date2 = time.strftime("%a %d %B %Y")
                con = psycopg2.connect("host=<host ip address> dbname=<database_name> user=<username> password=<password>")
                cur = con.cursor()
                cur.execute("INSERT INTO data_history(date_,time_,sensor1_temp,sensor2_temp,average_temp,fridge_on,low_low_alarm,high_high_alarm) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(date1,time1,readHRRegs[0],readHRRegs[1],readHRRegs[19],readFromDiscrete_Inputs[0],readFromCoils[0],readFromCoils[1]))
                cur.execute("UPDATE current_data SET date_ = %s,time_ = %s,sensor1_temp = %s,sensor2_temp = %s,average_temp = %s,fridge_on = %s,low_low_alarm = %s,high_high_alarm = %s WHERE id = 1",(date1,time1,readHRRegs[0],readHRRegs[1],readHRRegs[19],readFromDiscrete_Inputs[0],readFromCoils[0],readFromCoils[1]))
                cur.execute("SELECT * FROM threshold_variables ORDER By id ASC")
                RawResult = cur.fetchall()
                con.commit()
                cur.close()
                con.close()
                time.sleep(0.1)
                regvalue1 = ((float(RawResult[0][2]))/((float(150)/410)/10))
                regvalue2 = ((float(RawResult[1][2]))/((float(150)/410)/10))
                regvalue3 = ((float(RawResult[2][2]))/((float(150)/410)/10))
                regvalue4 = ((float(RawResult[3][2]))/((float(150)/410)/10))
                address1 = int(configuration[4][2]) + 16
                client.write_register(address1,regvalue1)
                address2 = int(configuration[4][2]) + 17
                client.write_register(address2,regvalue2)
                address3 = int(configuration[4][2]) + 18
                client.write_register(address3,regvalue3)
                address4 = int(configuration[4][2]) + 20
                client.write_register(address4,regvalue4)
                polltime = int(configuration[1][2]) - 1
                if polltime <= 0:
                    polltime = 1
                time.sleep(polltime)
                ###########################################################
                ##########RESET POLL CYCLE ERRORS AND OK STATUS############
                ###########################################################
                #Reset pollOk to 0; Ensure that there are 10 OK Polls before reseting pollError
                if (pollOk == 10):#after 10 correct polls reset pollError to 0
                    if pollError >= 10:
		    	errorText = "Recovery: io_Polling Module Error recovered"
                    	logWrite(errorText)
                    	Send_Alarm_Email("Recovery of Brewery io_Polling Module error ",errorText,configuration)
		    	pollError = 0
		if (pollOk < 15):
                    pollOk += 1
                #counterA += 1#Disabled for use other wise till time out polling after
        ###################################################################
        ###########################CATCH ERRORS############################
        ###################################################################
        except pymodbus.exceptions.ConnectionException:
            #Failed to connect to Modbus Client
            if pollError == 10: #must have 10 errors in a row
		errorText = "Error: Failed to connect to Modbus Client"
                logWrite(errorText)
		Send_Alarm_Email("Brewery Modbus Failure",errorText,configuration)
		pollOk = 0
            pollError += 1
            time.sleep(1)
        except AttributeError:
            #Failed to read Modbus register
            if pollError == 10: #must have 10 errors in a row
		errorText = "Error: Incorrect Modbus Register Read"
                logWrite(errorText)
		Send_Alarm_Email("Failure Reading Modbus Register",errorText,configuration)
		pollOk = 0
            pollError += 1
            time.sleep(1)
        except TypeError:
            #Incorrect data type
            if pollError == 10: #must have 10 errors in a row
		errorText = "Error: Incorrect data type in io_Polling Module"
                logWrite(errorText)
		Send_Alarm_Email("Failure Incorrect datatype io_Polling Module",errorText,configuration)
    		pollOk = 0
            pollError += 1
            time.sleep(1)



