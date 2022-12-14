# #!/usr/bin/env python

import can
import inputs
import math
from inputs import get_gamepad

joystick_pos = 0.0 # Scaled value of Xbox joystick, from [-1.0, 1.0]
steering_angle = None #from [0,255], theoretically. Actual limit is calibrated per-vehicle.

def parse_msgs(msg1_data: bytearray, msg2_data: bytearray) -> str:
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
    # print(selected_map)
    return f"{torque},{duty},{current},{supply_voltage/10},{switch_pos},{temp},{torque_a},{torque_b},{angle},{analog_c1},{analog_c2},{selected_map},{errors},{dio_bitfield},{status_bitfield},{limit_bitfield}\n"
    # return f"{torque_a}, {torque_b}\n"


with can.interface.Bus(bustype='slcan', channel='COM3', bitrate=500000, receive_own_messages=True) as bus:
    with open('out.csv', 'w') as f:
        # CSV file header
        f.write('Torque,Duty %,Current (A),Supply Voltage (V), Switch pos, Temp (C), Torque A, Torqe B, Angle, Analog C1, Analog C2, Map, Errors, DIO, Status, Limit\n')

        cached_msg1 = None

        # data = 0x059e610000000000


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
                    f.write(parse_msgs(cached_msg1, msg.data))
            # else:
                # print(f"{msg.arbitration_id}: {list(msg.data)}")

            events = get_gamepad()
            for event in events:
                if str(event.code) == "ABS_X":
                    joystick_pos = event.state / 32800 # Divide by joystick-specific max value
                    print(joystick_pos)

                    # We need to map [-1.0, 1.0] to [0, 255]
                    torqueA: int = math.ceil((joystick_pos+1) * (255/2))
                    torqueB: int = 255-torqueA

                    data = [0x03, torqueA, torqueB, 0x00, 0x00, 0x00, 0x00, 0x00]
                    message = can.Message(arbitration_id=0x296, data=data, check=True, is_extended_id=False)
                    bus.send(message, timeout=0.2)
                # print(event.ev_type, event.code, event.state)


            