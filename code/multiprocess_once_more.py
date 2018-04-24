# -*- coding: utf-8 -*-
from multiprocessing import Process, Manager, Lock
import time

manager = Manager()
sum = manager.Value('tmp', 0)
lock = Lock()


class ScheduleTest():
    @staticmethod
    def printx():
        while True:
            print('hello x')
            time.sleep(5)

    def run(self):
        with lock:
            if not sum.value:
                print('printx is running...')
                my_process = Process(target=self.printx)
                my_process.start()
                sum.value += 1
            else:
                print('printx has ran.')


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
