#!/usr/bin/env python


import PeriodicTimer
import time

pt = PeriodicTimer.PeriodicTimer()

pt.start()


while True:
    print(PeriodicTimer.counter)
    time.sleep(5.0)
