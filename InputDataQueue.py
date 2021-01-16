#!/usr/bin/env python


##
#  @package InputDataQueue Module contains the FIFO queue declarations which hold the
#  different types of data acquired
#


import queue

##
#  Queue containing the modbus response list
modbusDataQueue = queue.Queue()

##
# Queue containing the incoming jobs for the serial communication
serialJobQueue = queue.Queue()

