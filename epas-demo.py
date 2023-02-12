# #!/usr/bin/env python

import can
# import inputs
import math
# from inputs import get_gamepad

class Controller:
    joystick_pos = 0.0 # Scaled value of Xbox joystick, from [-1.0, 1.0]
    limit_left:int = 19
    limit_right: int = 230
    steering_angle = 0.0 #from [0,255], theoretically. Actual limit is calibrated per-vehicle.

    def parse_msgs(self, msg1_data: bytearray, msg2_data: bytearray) -> str:
        torque = msg1_data[0]
        duty = msg1_data[1]
        current = msg1_data[2]
        supply_voltage = msg1_data[3]
        switch_pos = msg1_data[4]
        temp = msg1_data[5]
        torque_a = msg1_data[6]
        torque_b = msg1_data[7]
        
        angle = msg2_data[0]
        analog_c1 = msg2_data[1]
        analog_c2 = msg2_data[2]
        selected_map = msg2_data[3]
        errors = msg2_data[4]
        dio_bitfield = msg2_data[5]
        status_bitfield = msg2_data[6]
        limit_bitfield = msg2_data[7]
        self.steering_angle = angle
        # print(selected_map)
        return f"{torque},{duty},{current},{supply_voltage/10},{switch_pos},{temp},{torque_a},{torque_b},{angle},{analog_c1},{analog_c2},{selected_map},{errors},{dio_bitfield},{status_bitfield},{limit_bitfield}\n"
        # return f"{torque_a}, {torque_b}\n"

    def send_command(self, bus):
        current_angle_normalized = ((self.steering_angle-self.limit_left)/(self.limit_right-self.limit_left)*2)-1
        

        e = 0.0 - current_angle_normalized # Error = target - current

        # We need to map [-1.0, 1.0] to [0, 255]

        power = e # Power is an abstract value from [-1., 1.], where -1 is hard push left.

        torqueA: int = min(255,max(0, math.ceil((power+1) * (255/2))))
        torqueB: int = 255-torqueA

        print (f"{torqueA}")

        data = [0x03, torqueA, torqueB, 0x00, 0x00, 0x00, 0x00, 0x00]
        message = can.Message(arbitration_id=0x296, data=data, check=True, is_extended_id=False)
        bus.send(message, timeout=0.2)

        print (f"{torqueA}")
        # print(e)

    def run(self, channel='COM1'):
        with can.interface.Bus(bustype='slcan', channel=channel, bitrate=500000, receive_own_messages=True) as bus:
         
            cached_msg1 = None

            while (True):
                # bus.send(message, timeout=0.2)
                # print(f"Sending {message}")
                msg = bus.recv(0.2)
                if (msg is None):
                    print("Skipping")
                elif (msg.arbitration_id == 0x290):
                    cached_msg1 = msg.data
                elif(msg.arbitration_id == 0x292):
                    if (cached_msg1 is not None):
                        self.parse_msgs(cached_msg1, msg.data)

                # events = get_gamepad()
                # for event in events:
                #     if str(event.code) == "ABS_X":
                #         self.joystick_pos = event.state / 32800 # Divide by joystick-specific max value
                self.send_command(bus)

if __name__ == "__main__":
    controller = Controller()
    controller.run('/dev/serial/by-id/usb-Protofusion_Labs_CANable_1205aa6_https:__github.com_normaldotcom_cantact-fw_001500174E50430520303838-if00')