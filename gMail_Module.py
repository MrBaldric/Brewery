#Email Module for using "The Mouldystalk Brewery Gmail account"
# Need to chanage the file location details on file attached function

import smtplib,email,email.encoders,email.mime.text,email.mime.base
from email.mime.multipart import MIMEMultipart
from error_Logging import logWrite

def emailText(subject,body,toAddress):
    fromAddr = "from_address_here@gmail.com>"
    emailMsg = email.MIMEMultipart.MIMEMultipart('mixed')
    emailMsg['Subject'] = subject
    emailMsg['From'] = fromAddr
    emailMsg['To'] = toAddress
    emailMsg.attach(email.mime.text.MIMEText(body,'html'))
    username = "username@gmail.com"
    password = "password"

    try:
        gmailServer = smtplib.SMTP("smtp.gmail.com:587")
        gmailServer.starttls()
        gmailServer.login(username, password)
        gmailServer.sendmail(fromAddr, toAddress,emailMsg.as_string())
        gmailServer.quit()
        logWrite("EMail: Successfully sent email Alert")
    except Exception:
        logWrite("Error: unable to send email Alert")


def DailyReportEmail(fileLoc,filename,toAddress):
    body = """\
    <b><p style="color:green;font-size:120%">Welcome to the MouldyStalk Brewery
    <br>===============================
    <br>Daily Report</p></b>
    <br><i><p>Please see attached the Daily Brewery Report
    <br><br>Thank you<br><br>Have a great day</p></i>
    """
    toAddr = toAddress
    fromAddr = "from_address_here@gmail.com>"
    emailMsg = MIMEMultipart()
    emailMsg['Subject'] = "Daily Report"
    emailMsg['From'] = fromAddr
    emailMsg['To'] = toAddr
    loadFile = open('{}{}'.format(fileLoc,filename), 'rb')
    filetitle ="Daily Brewery Report.pdf"
    emailMsg.attach(email.mime.text.MIMEText(body,'html'))
    fileMsg = email.mime.base.MIMEBase('application','pdf')
    fileMsg.set_payload((loadFile).read())
    fileMsg.add_header('Content-Disposition', 'attachment', filename = filetitle)
    email.encoders.encode_base64(fileMsg)
    emailMsg.attach(fileMsg)
    loadFile.close()
    username = "username_here@gmail.com"
    password = "password"

    try:
        gmailServer = smtplib.SMTP("smtp.gmail.com:587")
        gmailServer.starttls()
        gmailServer.login(username, password)
        gmailServer.sendmail(fromAddr, toAddr,emailMsg.as_string())
        gmailServer.quit()
        logWrite("EMail: Successfully sent Daily Email Report")
    except Exception:
        logWrite("Error: unable to send email Report")