# #!/usr/bin/env python

import math
import time

import can
import inputs
from inputs import get_gamepad
import numpy as np
from tqdm import trange, tqdm

COMMAND_ID = 0xFF0000
REPORT_ID = 0xFF0001


class LAController:

    def parseResponseMsg(self, msg: can.Message):
        if msg.data[0] == 0x98 and msg.data[1] == 0x00:
            self.parseEPR(msg)

        else:
            print(msg)

    def parseEPR(self, msg: can.Message):
        """Parse an Enhanced Position Report message

        Args:
            msg (can.Message): EPR message

        EPR message format:
        [0x98 0x00 ShaftA ShaftB Errors CurrentA CurrentB Status]
        """

        data = msg.data

        # Parse int from shaftA, shaftB
        shaft_extension_inches = int.from_bytes(
            data[2:4], byteorder='little')*0.001

        # Parse errors
        fault_code = data[4]
        is_faulty = fault_code > 0  # True if one of the bit flags is set

        # Parse current
        current_mA = int.from_bytes(data[5:7], byteorder='little')

        print(
            f"Pos: {shaft_extension_inches} inches, status: {fault_code}, current: {current_mA} mA")

    def enableClutch(self, bus: can.Bus):
        clutch_enable = True
        motor_enable = False
        clutch_enable_byte = clutch_enable * 0x80
        motor_enable_byte = motor_enable * 0x40
        byte3 = clutch_enable_byte + motor_enable_byte

        data = [0x0F, 0x4A, 0, byte3, 0, 0, 0]

        message = can.Message(
            arbitration_id=COMMAND_ID, data=data, is_extended_id=True)

        msg = bus.recv(0.1)
        return msg

    def disableClutch(self, bus: can.Bus):
        clutch_enable = False
        motor_enable = False
        clutch_enable_byte = clutch_enable * 0x80
        motor_enable_byte = motor_enable * 0x40
        byte3 = clutch_enable_byte + motor_enable_byte

        data = [0x0F, 0x4A, 0, byte3, 0, 0, 0]

        message = can.Message(
            arbitration_id=COMMAND_ID, data=data, is_extended_id=True)

        msg = bus.recv(0.1)
        return msg


    def sendToPosition(self, pos: float, bus: can.Bus):
        """Given position, send appropriate CAN messages to LA

        Args:
            pos (float): Position from 0.0 (fully extended) to 1.0 (fully retracted)

        Position command format:
        [0x0F 0x4A  DPOS_LOW Byte3 0 0 0 0]

        Byte 3:
        [ClutchEnable MotorEnable POS7 POS6 POS5 POS4 POS3]
        """

        POSITION_MAX = 3.45
        POSITION_MIN = 0.80
        range = POSITION_MAX - POSITION_MIN
        pos_inches = pos * range + POSITION_MIN

        # Account for 0.5 inch offset
        pos_value = int(pos_inches * 1000) + 500

        dpos_hi = int(pos_value / 0x100)
        dpos_low = pos_value % 0x100

        clutch_enable = True
        motor_enable = True
        clutch_enable_byte = clutch_enable * 0x80
        motor_enable_byte = motor_enable * 0x40
        byte3 = sum([dpos_hi, clutch_enable_byte, motor_enable_byte])

        data = [0x0F, 0x4A, dpos_low, byte3, 0, 0, 0]
        # print(hex(clutch_enable_byte))
        # print(hex(motor_enable_byte))
        # print(hex(byte3))

        message = can.Message(
            arbitration_id=COMMAND_ID, data=data, is_extended_id=True)

        bus.send(message)

        msg = bus.recv(0.1)

        return msg

    def run(self, channel, bitrate):
        print("Opening bus... ", end="")
        bus = can.interface.Bus(
            bustype='slcan', channel=channel, bitrate=bitrate, receive_own_messages=True)
        print("Bus open.")

        x = np.linspace(0.0, 4*np.pi, 201)
        positions = (np.sin(x) + 1.0) / 2
        print(positions)

        self.enableClutch(bus=bus)

        for pos in tqdm(positions):
            response = self.sendToPosition(pos, bus=bus)
            time.sleep(0.05)
            # print(pos, end=" ")
            # self.parseResponseMsg(response)

        self.disableClutch(bus=bus)

        # self.sendToPosition(0.0, bus=bus)
        # time.sleep(0.4)
        # self.sendToPosition(0.5, bus=bus)
        # time.sleep(1.4)
        # self.sendToPosition(1.0, bus=bus)
        # time.sleep(2.4)


if __name__ == "__main__":
    controller = LAController()
    controller.run('/dev/ttyACM0', bitrate=250000)
