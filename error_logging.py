#used to log errors into sql from all modules
import psycopg2
import time

def logWrite(errorText):
    date1 = time.strftime("%Y-%m-%d")
    time1 = time.strftime("%H:%M:%S")
    con = psycopg2.connect("host=<host ip address> dbname=<database_name> user=<username> password=<password>")
    cur = con.cursor()
    cur.execute("INSERT INTO log(date_,time_,description) VALUES(%s,%s,%s)",(date1,time1,errorText))
    con.commit()
    cur.close()
    con.close()