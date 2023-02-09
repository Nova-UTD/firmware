# Throttle By Wire in Circuit Python 
# ex. 5000 / 64 = 78, and 78 / 1024 * 3.3V = 0.25V output.

import board
from analogio import AnalogOut
# import time

def calc_volt(volt):
    return ((volt / 3.3) * 1024) * 64

def voltage(x):
    volt_o = (0.1809*x) + 0.8335
    volt_b = (0.3949*x) + 1.6996
    return volt_o, volt_b

analog_outO = AnalogOut(board.A0)
analog_outB = AnalogOut(board.A1)

while (True):
    input_num = float(input('Enter num between 0 and 1: '))
    volt = voltage(input_num)
    analog_outO.value = int(calc_volt(volt[0]))
    analog_outB.value = int(calc_volt(volt[1]))
    print(volt[0])
    print(volt[1])
