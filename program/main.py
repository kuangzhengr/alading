import main_controller


thread1 = main_controller.Server()
thread2 = main_controller.MainProgram()

thread1.start()
thread2.start()
thread1.join()
thread2.join()