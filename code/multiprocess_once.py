# -*- coding: utf-8 -*-
from multiprocessing import Process, Semaphore
import time


s = Semaphore(1)


class ScheduleTest():
    @staticmethod
    def printx():
        while True:
            print('hello x')
            time.sleep(5)

    def run(self):
        s.acquire()
        print('printx is running...')
        my_process = Process(target=self.printx)
        my_process.start()
        my_process.join()
        s.release()


def app_run():
    my_schedule = ScheduleTest()
    process_0 = Process(target=my_schedule.run)
    process_1 = Process(target=my_schedule.run)
    process_2 = Process(target=my_schedule.run)
    process_0.start()
    process_1.start()
    process_2.start()


if __name__ == '__main__':
    app_run()
