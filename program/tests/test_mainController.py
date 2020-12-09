import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import unittest
import main_controller
import Product
import os
import json
import requests

class testNotifyer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_serverclass(self):
        thread = main_controller.Server()
        thread.start()
        res = requests.get("http://localhost:8000/")
        self.assertEqual(200, res.status_code)
        thread.shutDown()
        thread.join()


    def test_mainProgram(self):
        mainProgram = main_controller.MainProgram()
        interval = mainProgram.getInterval()
        self.assertTrue(type(interval) == int or type(interval) == float)
        self.assertTrue(mainProgram.sleep(0))
        self.assertTrue(mainProgram.startChecking())



if __name__ == '__main__':
    unittest.main()