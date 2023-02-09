# Throttle By Wire in Circuit Python
# download the CircuitPython Analog Out libraries
# ex. 5000 / 64 = 78, and 78 / 1024 * 3.3V = 0.25V output.
# 1.55V = 30782
# 2.0V = 39718

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
    input_num = input('Enter num between 0 and 1: ')
    if input_num[0] == 't':
        num = float(input_num[1:])
        volt = voltage(num)
        analog_outO.value = int(calc_volt(volt[0]))
        analog_outB.value = int(calc_volt(volt[1]))
        print(volt[0])
        print(volt[1])
