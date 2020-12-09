import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import unittest
import ProgramChecker
import main_controller

class testProgramChecker(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.checker = ProgramChecker.ProgramChecker()


    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_generateNotifyMessage(self):
        msg = self.checker.generateNotifyMessage()
        self.assertTrue(type(msg) == str)

    def test_notifySysOperator(self):
        self.assertFalse(self.checker.notifySysOperator())

    def test_checkProgramStatus(self):
        self.assertFalse(self.checker.checkProgramStatus())

        thread = main_controller.Server()
        thread.start()
        self.assertTrue(self.checker.checkProgramStatus())
        thread.shutDown()
        thread.join()


if __name__ == '__main__':
    unittest.main()