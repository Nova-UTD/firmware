'''
Test code to reverse engineer the CAN messages on the Polaris GEM e6

Suspected IDs:
83825408
150931439
217056256
218042099
218064384

Author: Will Heitman
'''

import can

with can.interface.Bus(bustype='slcan', channel="COM4", bitrate=250000, receive_own_messages=True) as bus:
    
    f1 = open('83825408.csv', 'w')
    f2 = open('150931439.csv', 'w')
    f3 = open('217056256.csv', 'w')
    f4 = open('218042099.csv', 'w')
    f5 = open('218064384.csv', 'w')
    
    with open('gem_msgs.csv', 'w') as f:
        # CSV file header
        f.write('ID, b0, b1, b2, b3, b4, b5, b6, b7\n')

        cached_msg1 = None

        i = 0

        while (True):

            msg = bus.recv(0.1)

            if msg is not None and msg.arbitration_id==217056256:
                    # for byte in list(msg.data):
                    #     f3.write(f"{byte},")
                    # f3.write("\n")
                print(list(msg.data))

        # while (i < 5000):
        #     # bus.send(message, timeout=0.2)
        #     # print(f"Sending {message}")
        #     msg = bus.recv(0.2)
        #     if msg is not None:

        #         if msg.arbitration_id==83825408:
        #             for byte in list(msg.data):
        #                 f1.write(f"{byte},")
        #             f1.write("\n")
        #         elif msg.arbitration_id==150931439:
        #             for byte in list(msg.data):
        #                 f2.write(f"{byte},")
        #             f2.write("\n")
        #         elif msg.arbitration_id==217056256:
        #             # for byte in list(msg.data):
        #             #     f3.write(f"{byte},")
        #             # f3.write("\n")
        #             print(msg.data[4])
        #         elif msg.arbitration_id==218042099:
        #             for byte in list(msg.data):
        #                 f4.write(f"{byte},")
        #             f4.write("\n")
        #         elif msg.arbitration_id==218064384:
        #             for byte in list(msg.data):
        #                 f5.write(f"{byte},")
        #             f5.write("\n")
        #     i += 1

    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()
                