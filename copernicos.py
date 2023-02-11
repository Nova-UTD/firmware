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
from io import StringIO

import board
from analogio import AnalogOut
import neopixel
import digitalio

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

    def setThrottle(throttle_value: float):
        """Sets voltage lines to emulate throttle pedal

        Args:
            throttle_value (float): Between 0.0-1.0, where 1.0 is full throttle.
        """

        # Voltages for channels 1 and 2 of the
        # accelerator position sensor (APS)
        volt_c1 = (0.1809*throttle_value) + 0.8335
        volt_c2 = (0.3949*throttle_value) + 1.6996

    async def spin(self):
        
        input = ''
        line = ''
        index = 0
        ctrl_c_seen = False

        while True:                         # for each line
            try:
                led_task = asyncio.create_task(self.setStatusLed())
                await asyncio.gather(led_task)
            #     index = 0
            #     line = ''

            #     while True:                   # for each character
            #         ch = ord(sys.stdin.read(1))

            #         if 32 <= ch <= 126:           # printable character
            #             line = line[:index] + chr(ch) + line[index:]
            #             index += 1

            #         elif ch in {10, 13}:          # EOL - try to process
            #             if input:
            #                 input = input + ' ' + line.strip()
            #             else:
            #                 input = line.strip()
            #             line = ''
            #             try:
            #                 print(f"\nParsing command '{input}'")
            #                 input = ''
            #             except SyntaxError as e:
            #                 if str(e) != 'unexpected EOF in list':
            #                     sys.stdout.write('\n')
            #                     sys.stdout.write(str(e))
            #                     input = ''
            #             sys.stdout.write('\n')
            #             break

            #         #####################

            #         elif ch == 1:             # CTRL-A: start of line
            #             index = 0

            #         elif ch == 5:             # CTRL-E: end of line
            #             index = len(line)

            #         #####################

            #         elif ch == 2:             # CTRL-B: back a word
            #             while index > 0 and line[index-1] == ' ':
            #                 index -= 1
            #             while index > 0 and line[index-1] != ' ':
            #                 index -= 1

            #         elif ch == 6:             # CTRL-F: forward a word
            #             while index < len(line) and line[index] == ' ':
            #                 index += 1
            #             while index < len(line) and line[index] != ' ':
            #                 index += 1

            #         #####################

            #         elif ch == 4:             # CTRL-D: delete forward
            #             if index < len(line):
            #                 line = line[:index] + line[index+1:]

            #         elif ch == 11:            # CTRL-K: clear to end of line
            #             line = line[:index]

            #         elif ch in {8, 127}:     # backspace/DEL
            #             if index > 0:
            #                 line = line[:index - 1] + line[index:]
            #                 index -= 1

            #         #####################

            #         elif ch == 20:            # CTRL-T: transpose characters
            #             if index > 0 and index < len(line):
            #                 ch1 = line[index - 1]
            #                 ch2 = line[index]
            #                 line = line[:index - 1] + \
            #                     ch2 + ch1 + line[index + 1:]

            #         #####################

            #         elif ch == 27:            # ESC
            #             next1, next2 = ord(sys.stdin.read(1)), ord(
            #                 sys.stdin.read(1))
            #             if next1 == 91:           # [
            #                 if next2 == 68:       # left arrow
            #                     if index > 0:
            #                         index -= 1
            #                     else:
            #                         sys.stdout.write('\x07')
            #                 elif next2 == 67:     # right arrow
            #                     if index < len(line):
            #                         index += 1
            #                     else:
            #                         sys.stdout.write('\x07')

            #         else:
            #             print('Unknown character: {0}'.format(ch))

            #         # Update screen
            #         sys.stdout.write("\x1b[1000D")  # Move all the way left
            #         sys.stdout.write("\x1b[0K")    # Clear the line
            #         sys.stdout.write(line)
            #         # Move all the way left again
            #         # sys.stdout.flush()
            except Exception as e:
                sys.stdout.write('\n')
                print(e)
                sys.stdout.write('\n')
                input = ''


if __name__ == '__main__':

    os = CopernicOS()

    asyncio.run(os.spin())
