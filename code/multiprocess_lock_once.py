# -*- coding: utf-8 -*-
from multiprocessing import Process, Lock
import time


lock = Lock()

class ScheduleTest():
    @staticmethod
    def printx():
        while True:
            print('hello x')
            time.sleep(5)

    def run(self):
        print('printx is running...')
        my_process = Process(target=self.printx)
        my_process.start()


def app_run():
    my_schedule = ScheduleTest()
    for i in range(3):
        with lock:
            p = Process(target=my_schedule.run)
            p.start()
            p.join()


if __name__ == '__main__':
    app_run()
