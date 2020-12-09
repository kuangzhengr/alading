import requests
import sys
import Notifyer
from datetime import date
from datetime import datetime

"""
this class is aim to monitor the status of the policy-checking program
"""
class ProgramChecker(object):
    def __init__(self):
        self.checkInterval = 20

    def generateNotifyMessage(self):
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

    def notifySysOperator(self):
        """
        Sending an email to system operator to notify the program is not running
        """
        msg = self.generateNotifyMessage()
        print(msg)
        # with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        #         smtp.ehlo()
        #         smtp.starttls()
        #         smtp.ehlo()

        #         smtp.login("aladinshixi@gmail.com", "qwerQWER123.")

        #         smtp.sendmail("aladinshixi@gmail.com", "aladinshixi@gmail.com", msg)

        #         smtp.close()
        return False

    def checkProgramStatus(self):
        try:
            res = requests.get("http://localhost:8000/")
            if (res.status_code != 200):
                return self.notifySysOperator()
            else:
                print("program is running.")
                return True
        except requests.exceptions.RequestException as e:
            return self.notifySysOperator()

