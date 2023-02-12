"""
 .    '                   .  "   '
                                        "                  "             '
      ,    /),      `          _____              *             _       ____   _____ 
 .   (( -.((_))  _,)   *      / ____|                          (_)     / __ \ / ____|
     ,\`.'    `-','          | |     ___  _ __   ___ _ __`_ __  _  ___| |  | | (___  
     `.>        (,-          | |    / _ \| '_ \ / _ \ '__| '_ \| |/ __| |  | |\___ \ 
    ,',          `._,)       | |___| (_) | |_) |  __/ |  | | | | | (__| |__| |____) |
   ((  )        (`--'      '  \_____\___/| .__/ \___|_|  |_| |_|_|\___|\____/|_____/ 
    `'( ) _--_,-.\              `       | |                     *
       /,' \( )  `' sst                 |_|          .
      ((    `\     .                                        .             '
       `                                    *                    `

=Nova at UT Dallas=

Real-time operating script for CircuitPython-based microcontrollers

See readme for more information.
"""
import asyncio
import gc
import sys
import time
from io import StringIO

import board
from analogio import AnalogOut
import neopixel
import digitalio
import supervisor # serial_bytes_available()

VERSION = "1.0"

# REPL history support

history_max_size = 40
history = []

APS_CH1_PIN = board.A0
APS_CH2_PIN = board.A1


# def calc_volt(volt) -> int:
#     return ((volt / 3.3) * 1024) * 64


# def voltage(x):
#     volt_o = (0.1809*x) + 0.8335
#     volt_b = (0.3949*x) + 1.6996
#     return volt_o, volt_b


# analog_outO = AnalogOut(board.A0)
# analog_outB = AnalogOut(board.A1)
# # while (True):
# #     input_num = input('Enter num between 0 and 1: ')
# #     if input_num[0] == 't':
# #         num = float(input_num[1:])
# #         volt = voltage(input_num)
# #         analog_outO.value = int(calc_volt(volt[0]))
# #         analog_outB.value = int(calc_volt(volt[1]))
# #         print(volt[0])
# #         print(volt[1])


class SystemStatus:
    IDLE = 0
    ACTIVE = 1
    WARN = 2
    FAULTY = 3

class Error:
    invalid_input = False

    def __init__(self, invalid_input = False):
        invalid_input = invalid_input

    def getBinary(self):
        return bin(int(self.invalid_input))

class CopernicOS:

    def __init__(self):
        print(f'==         CopernicOS v{VERSION}          ==')
        print(f'~~        {gc.mem_free()} bytes free         ~~')
        print(f'~~ Nova at UTD - nova-utd.github.io ~~\n')

        self.status: SystemStatus = SystemStatus.IDLE

        # Set I/O
        self.aps_c1_out = AnalogOut(APS_CH1_PIN)
        self.aps_c2_out = AnalogOut(APS_CH2_PIN)
        self.status_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.status_pixel.brightness = 0.3
        print("* IO has been configured")

        # Control variables
        self.target_throttle = 0.0
        self.command_str = ""

        # Safety variables
        self.THROTTLE_INPUT_TIMEOUT = 0.5 # sec
        self.last_throttle_input_time: float = -1.0

    async def setStatusLed(self):
        """Sets the built-in neopixel according to system status
        """
        if self.status == SystemStatus.IDLE:
            self.status_pixel.fill((0, 255, 255))
        elif self.status == SystemStatus.FAULTY:
            self.status_pixel.fill((255, 0, 0))
        elif self.status == SystemStatus.ACTIVE:
            self.status_pixel.fill((0, 255, 0))
        elif self.status == SystemStatus.WARN:
            self.status_pixel.fill((255, 200, 0))

        await asyncio.sleep(0.5)

    async def checkForInput(self):
        if not supervisor.runtime.serial_connected:
            # USB serial not available
            self.status = SystemStatus.WARN
            return
        if not supervisor.runtime.serial_bytes_available:
            # No serial data in buffer
            await asyncio.sleep(0.05)
            return


        while supervisor.runtime.serial_bytes_available:
            char = sys.stdin.read(1)
            self.command_str += char
            if char == '$':
                # Beginning of new command
                self.command_str = ""
            elif char == ';':
                # Command is complete
                self.command_str = self.command_str[:-1]
                parts = self.command_str.split(',')
                self.target_throttle = float(parts[1])
                self.last_throttle_input_time = time.time()

                # Flush the buffer
                trash = input()

                print(self.command_str)
            
            
        # print(self.command_str)
        return
        
        # Parse the input
        command_str = input()
        parts = command_str.split(',')
        if len(parts) < 2:
            print("Error: Commands must have at least 2 parts")
            return

        if parts[0].lower() == 'throttle':
            print(parts[1])
            print(f"Setting throttle to {float(parts[1])}")
            # self.setThrottle(float(parts[1]))
            self.target_throttle = float(parts[1])
            self.last_throttle_input_time = time.time()
        else:
            print("Error: Unrecognized command.")
            return

    async def setThrottle(self,):
        """Sets voltage lines to emulate throttle pedal

        Args:
            throttle_value (float): Between 0.0-1.0, where 1.0 is full throttle.
        """

        # Compare current time with time last input was received
        dt = time.time() - self.last_throttle_input_time
        if dt > self.THROTTLE_INPUT_TIMEOUT:
            self.target_throttle = 0.0
            self.status = SystemStatus.IDLE
        else:
            self.status = SystemStatus.ACTIVE

        # Voltages for channels 1 and 2 of the
        # accelerator position sensor (APS)
        volt_c1 = (0.1809*self.target_throttle) + 0.8335
        volt_c2 = (0.3949*self.target_throttle) + 1.6996

        self.aps_c1_out.value = int(((volt_c1 / 3.3) * 1024) * 64)
        self.aps_c2_out.value = int(((volt_c2 / 3.3) * 1024) * 64)

    async def spin(self):
        
        input = ''
        line = ''
        index = 0
        ctrl_c_seen = False

        while True:                         # for each line
            try:
                led_task = asyncio.create_task(self.setStatusLed())
                serial_input_task = asyncio.create_task(self.checkForInput())
                throttle_control_task = asyncio.create_task(self.setThrottle())
                await asyncio.gather(led_task, serial_input_task)
            except Exception as e:
                sys.stdout.write('\n')
                print(e)
                sys.stdout.write('\n')
                input = ''


if __name__ == '__main__':

    os = CopernicOS()

    asyncio.run(os.spin())
