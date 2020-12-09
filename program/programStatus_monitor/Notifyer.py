import smtplib

class Notifyer(object):
    def __init__(self, violations):
        self.violations = violations 

    def sendNotificationmails(self):
        for store_violation in self.violations:
            if (len(self.violations[store_violation]) > 0):
                subject = "violation notification - " + str(store_violation)[:-5]
                body = ""
                for singleViolation in self.violations[store_violation]:
                    body += singleViolation
                    body += "\n"
                
                msg = f'Subject: {subject} \n\n{body}'
                print("Message going to be sent: \n")
                print(msg)
                self.sendMail(msg)
        
        return True


    def sendMail(self, msg):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login("aladinshixi@gmail.com", "qwerQWER123.")
            smtp.sendmail("aladinshixi@gmail.com", "aladinshixi@gmail.com", msg)
            smtp.close()

            return True