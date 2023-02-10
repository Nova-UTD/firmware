# #!/usr/bin/env python

import math
import time

import can
import inputs
from inputs import get_gamepad


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

    def sendToPosition(self, pos: float):
        """Given position, send appropriate CAN messages to LA

        Args:
            pos (float): Position from 0.0 (fully extended) to 1.0 (fully retracted)
        """
        request_confirmation = True
        request_auto_reply = True

    def run(self, channel, bitrate):
        with can.interface.Bus(bustype='slcan', channel=channel, bitrate=bitrate, receive_own_messages=True) as bus:
            with open('out.csv', 'w') as f:

                COMMAND_ID = 0xFF0000
                REPORT_ID = 0xFF0001

                # Just enable clutch
                command_data = [0x0F, 0x4A, 0xC4, 0x89, 0, 0, 0, 0]
                message = can.Message(
                    arbitration_id=COMMAND_ID, data=command_data, is_extended_id=True)
                bus.send(message)

                msg = bus.recv(0.2)
                if (msg is None):
                    print("Skipping")
                else:
                    self.parseResponseMsg(msg)

                time.sleep(0.025)

                # Clutch and motor on. Move to 2"
                command_data = [0x0F, 0x4A, 0xC4, 0x89, 0, 0, 0, 0]
                message = can.Message(
                    arbitration_id=COMMAND_ID, data=command_data, is_extended_id=True)
                bus.send(message)

                msg = bus.recv(0.2)
                if (msg is None):
                    print("Skipping")
                else:
                    self.parseResponseMsg(msg)

                time.sleep(1.0)

                # Clutch and motor on. Move to ?"
                command_data = [0x0F, 0x4A, 0xC4, 0x8F, 0, 0, 0, 0]
                message = can.Message(
                    arbitration_id=COMMAND_ID, data=command_data, is_extended_id=True)
                bus.send(message)

                msg = bus.recv(0.2)
                if (msg is None):
                    print("Skipping")
                else:
                    self.parseResponseMsg(msg)

                time.sleep(1.0)

                # Clutch and motor on. Move to 2"
                command_data = [0x0F, 0x4A, 0xC4, 0x89, 0, 0, 0, 0]
                message = can.Message(
                    arbitration_id=COMMAND_ID, data=command_data, is_extended_id=True)
                bus.send(message)

                msg = bus.recv(0.2)
                if (msg is None):
                    print("Skipping")
                else:
                    self.parseResponseMsg(msg)

                time.sleep(1.0)

                # Just enable clutch (again)
                command_data = [0x0F, 0x4A, 0xC4, 0x89, 0, 0, 0, 0]
                message = can.Message(
                    arbitration_id=COMMAND_ID, data=command_data, is_extended_id=True)
                bus.send(message)

                msg = bus.recv(0.2)
                if (msg is None):
                    print("Skipping")
                else:
                    self.parseResponseMsg(msg)

                time.sleep(0.025)

                # Disable clutch and motor
                command_data = [0x0F, 0x4A, 0xD0, 0x07, 0, 0, 0, 0]
                message = can.Message(
                    arbitration_id=COMMAND_ID, data=command_data, is_extended_id=True)
                bus.send(message)

                msg = bus.recv(0.2)
                if (msg is None):
                    print("Skipping")
                else:
                    self.parseResponseMsg(msg)


if __name__ == "__main__":
    controller = LAController()
    controller.run('/dev/ttyACM0', bitrate=250000)
