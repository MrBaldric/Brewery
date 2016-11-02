# Brewery
These files are part of my brewery monitoring program that I wrote completely from python.  It was the main starting point of my python writing.  Over time I have added bits and pieces with changes here and there.

The main basic setup is a Koyo 06 PLC used to monitor temperature using 4-20ma sensors and modbus tcp/ip being used to send the data back to a python and postgresql server for data logging.

Also I have used Tkinter for my GUI on the server for controlling the fermination temperature and email alarm temperature thresholds. 

There are daily reports that show the 24 hour temperature tracking as well as High and Low temperature alarts, as well as modbus tcp/ip failure alerts.  

Incorporated as well is a logging section that records successful emails sending, start and shutdown of the program as well as 
certain failures with in the program to help fault diagnostics.

I hope there are some parts that are useful to someone. cheers baldric
