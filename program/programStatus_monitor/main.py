import ProgramChecker
import time

checker = ProgramChecker.ProgramChecker()

while(True):
    checker.checkProgramStatus()
    time.sleep(checker.checkInterval)