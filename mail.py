#!/usr/bin/python
import os
import smtplib
import datetime
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
 
today = datetime.date.today()
fromaddr = "GIMECSystemsEngineering@tatacommunications.com"
toaddr = ["sathish.muniappan@tatacommunications.com"]
 
#output_files = [os.path.join(os.getcwd(), '../Output_files/JuniperSwitches_Summary_validated.csv')]
#output_names = ['JuniperSwitches_Summary_validated.csv']

def sendmail(host):
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = "Auto: Daily Connectivity count Details {:%d %b %Y}".format(today)
 
    body = """
        <head>
                <style>
                pre
                {
                font-family:Calibri;
                font-size:11pt;
                }
                </style>
        </head>
        <body>
        <p><pre><b>Hi,<br><br>
Please find the Daily Connectivity Report: <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; """
    content = host; 
    body1 = """<br><br><br>
            Regards,<br>
           GIMEC-Systems<br>
        <u>NOTE</u>:</b> This is an automated email<br><br><br><br><br><br><br>
<b><u>DISCLAIMER</u>:</b> You are reminded that the material being shared belongs to Tata Communications and contains sensitive information. Please ensure that you treat this material as confidential and do not forward or disclose any of the information contained herein to anyone outside Tata Communications.<br></pre></p>"""
 
    msg.attach(MIMEText(body+content+body1, 'html'))
    #fileMsg = email.mime.base.MIMEBase('application', 'vnd.ms-excel')
    #email.encoders.encode_base64(fileMsg)
    #fileMsg.add_header('Content-Disposition', 'attachment;filename=JuniperSwitches_Summary_validated.csv')
    #msg.attach(fileMsg)
 
 
    server = smtplib.SMTP('xx.xx.xx.xx')
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


if __name__ == '__main__':

    mail()
