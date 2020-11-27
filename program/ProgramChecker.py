import psutil
import sys
import time
import Notifyer
from datetime import date
from datetime import datetime

"""
this program is aim to monitor the status of the policy-checking program
pending implementation
"""

programName = 'main_controller.py'
checkInterval = 20

def generateNotifyMessage():
    """
    generate the warnning message with current date and time
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()
    current_date = today.strftime("%B %d, %Y")

    subject = "Progam operating warning - Not Running"
    body = "Since " + current_date + " at " + current_time 
    msg = f'Subject: {subject} \n\n{body}'
    return msg

def notifySysOperator():
    """
    Sending an email to system operator to notify the program is not running
    """
    msg = generateNotifyMessage()
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login("aladinshixi@gmail.com", "qwerQWER123.")

            smtp.sendmail("aladinshixi@gmail.com", "aladinshixi@gmail.com", msg)

            smtp.close()

def checkProgramStatus():
    """
    loop through all the current running process and see if the program is running
    """
    for process in psutil.process_iter():
        try:
            if len(process.cmdline()) > 1 and programName in process.cmdline()[-1]:
                print('Program is running.')
                return
        except(psutil.AccessDenied):
            pass

    notifySysOperator()


while(True):
    checkProgramStatus()
    time.sleep(checkInterval)