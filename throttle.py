# Throttle By Wire in Circuit Python
# ex. 5000 / 64 = 78, and 78 / 1024 * 3.3V = 0.25V output.
# you should upload the boot.py file
# boot.py should already be there 
# boot.py code:
# import usb_cdc
# usb_cdc.enable(console=True, data=True)

import board
from analogio import AnalogOut
import usb_cdc
import time

# global variables
# this serial variable should be an instance of a class, but it is returning NoneType
serial = usb_cdc.data
print(type(serial))
cur_time = time.time()
analog_outO = AnalogOut(board.A0)
analog_outB = AnalogOut(board.A1)


def calc_volt(volt):
    return ((volt / 3.3) * 1024) * 64


def voltage(x):
    volt_o = (0.1809*x) + 0.8335
    volt_b = (0.3949*x) + 1.6996
    return volt_o, volt_b


def move_throttle():
    data = check_buffer()
    update_lines(data)
    # use one millisecond (0.001)
    if (time.time() - cur_time) >= 5:
        update_lines('t0\n')


def check_buffer():
    if serial.in_waiting == 0:
        return
    # reads until a newline character (\n)
    data = serial.readline(size=-1)
    cur_time = time.time()
    return data


def update_lines(data):
    if data[0] == 't':
        num = float(data[1:-1])
        volt = voltage(num)
        analog_outO.value = int(calc_volt(volt[0]))
        analog_outB.value = int(calc_volt(volt[1]))


while (True):
    move_throttle()

