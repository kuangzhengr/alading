import json
import time
import os
import Product
import DataParsing
import DataChecking
import Notifyer
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.send_response(200)

        except:
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes('running', 'utf-8'))


class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.httpd = HTTPServer(('localhost', 8000), Serv)

    def run(self):
        self.httpd.serve_forever()

    def shutDown(self):
        self.httpd.shutdown()


class MainProgram(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.counter = 1
        self.flag = True

    def getInterval(self): 
        """
        get the interval in minutes from a json file
        """
        script_dir = os.path.dirname(__file__)
        script_dir += "\query_interval" 
        rel_path = "interval.json"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, 'rb') as f:
                interval_file = json.load(f)

        return interval_file["interval"]


    def sleep(self,interval):
        """
        put the program to sleep for 'interval' minutes
        """
        time.sleep(interval*60)
        return True



    def startChecking(self):
        """
        run the whole process of the program
        """
        interval = self.getInterval()
        print("running for check " + str(self.counter))
        self.counter += 1
        dataParsing = DataParsing.DataParsing()
        dataChecking = DataChecking.DataChecking(dataParsing.store_records)
        dataChecking.checkData()
        # notifyer = Notifyer.Notifyer(dataChecking.violation)
        # notifyer.sendNotificationmails()
        self.sleep(interval)
        return True

    def run(self):
        """
        while loop to run the whole process of the program forever
        """
        while (self.flag):
            self.startChecking()

    def shutDown(self):
        self.flag = False