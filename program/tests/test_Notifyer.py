import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import unittest
import Notifyer
import os
import json

class testNotifyer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.notifyer = Notifyer.Notifyer({
            "test_store.json" : ["test_store violation info"],
            "test_emptyStore.json" : []
            })

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sendNotificationmails(self):
        ## check mail box to see only one email(test_store) should be sent
        self.assertTrue(self.notifyer.sendNotificationmails())

    def test_sendMail(self):
        msg = f'Subject: {"test mail"} \n\n{"this is a test mail body"}'
        self.assertTrue(self.notifyer.sendMail(msg))



if __name__ == '__main__':
    unittest.main()