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

def speed(x):
    volt_o = (0.0095*x) + 0.7745
    volt_b = (0.0168*x) + 1.4956
    return [volt_o, volt_b]

analog_outO = AnalogOut(board.A0)
analog_outB = AnalogOut(board.A1)

while (True):
    input_speed = input('Enter speed: ')
    spd = speed(input_speed)
    analog_outO.value = int(calc_volt(spd[0]))
    analog_outB.value = int(calc_volt(spd[1]))
