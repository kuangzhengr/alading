import json
import time
import os
import Product
import DataParsing
import DataChecking
import Notifyer

def getInterval(): 
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


def sleep(interval):
    """
    put the program to sleep for 'interval' minutes
    """
    time.sleep(interval*60)


def run():
    """
    run the whole process of the program
    """
    interval = getInterval()
    coutner = 1
    while (True):
        print("running for check " + str(coutner))
        coutner += 1
        dataParsing = DataParsing.DataParsing()
        dataChecking = DataChecking.DataChecking(dataParsing.store_records)
        dataChecking.checkData()
        # notifyer = Notifyer.Notifyer(dataChecking.violation)
        # notifyer.sendNotificationmails()
        sleep(interval)


run()