# CAN buses
Hail-Bopp has two CAN buses. One is the CAN bus that came with our stock vehicle, and the other we added to support the EPAS and other peripherals.

We call the former the **GEM Bus**, as it is the default bus that came with the Polaris GEM e6.

We call the latter the **Robot Bus**, as it supports our autonomous functionality.

## GEM Bus
Bitrate is 250,000 bits per second.
> ⚠ If a device (e.g. a CANable) connects to the GEM Bus at a rate other than 250kBps, the vehicle ***will shut down***.

## Robot Bus
Bitrate is 500,000 bits per second.

## EPAS
Our Electronic Power Assisted Steering (EPAS) system is managed by an [EPAS18 Ultra](https://www.dcemotorsport.com/Home/EPASFileDownload?file=EPAS18_Ultra_User_Guide_V2.1_USA.pdf&site=us) controller. The Ultra acts as an intermediary between other CAN devices and the actual steering motor.

### Messages
The Ultra uses a 500kBps CAN connection with **non-extended (11-bit) message IDs**. To send a command to the EPAS using python-can, you must explicitly specify a non-extended ID.

Example:
```python
message = can.Message(arbitration_id=0x296, data=data, is_extended_id=False)
```

### CAN message #1: Incoming

- ID: 0x290 (decimal 656)

| Byte | Description                    |
| ---- | ------------------------------ |
| D0   | Torque (bits)                  |
| D1   | Motor duty (%)                 |
| D2   | Current (A)                    |
| D3   | Supply voltage (1 bit = 100mV) |
| D4   | Switch position (0 to 15)      |
| D5   | Box temp (celcius)             |
| D6   | Torque A (raw value in bits)   |
| D7   | Torque B (raw value in bits)   |



### CAN message #2: Incoming

- ID: 0x292 (decimal 658)

| Byte | Description                     |
| ---- | ------------------------------- |
| D0   | Steering angle (bits)           |
| D1   | Analog Channel 1 (bits)         |
| D2   | Analog Channel 2 (bits)         |
| D3   | Selected map (0-5)              |
| D4   | Error messages                  |
| D5   | Bit field of digital I/O values |
| D6   | Bit field of status flags       |
| D7   | Bit field of limit flags        |

#### Bit field of status flags:

- b0 – Program paused
- b1 – Motor moving forwards
- b2 – Motor moving in reverse
- b3 – Host mode active
- b4 – Fault light status
- b5 - Reserved
- b6 - Reserved
- b7 – Reserved

#### Bit field of limit flags: 

- b0 – Steering at LH stop
- b1 – Steering at RH stop
- b2 – Over-temperature condition
- b3 – Not used
- b4 – Not used
- b5 – Not used
- b6 – Not used
- b7 – Remote mode active

#### Error codes

- 100 Low battery voltage
- 101 Torque sensor not connected
- 102 Torque sensor fault
- 103 Current sensor fault
- 104 Motor power fault
- 105 Motor not connected
- 106 Motor is stalled or shorted
- 107 Clutch not connected
- 108 Clutch is stalled or shorted
- 109 Over current
- 110 Over temperature
- 111 Internal error

### CAN Message #3: Outgoing

Used to send out commands.

- ID: 0x296 (decimal 662)

| Byte | Description                                       |
| ---- | ------------------------------------------------- |
| D0   | Steering map (0 = local mode, 1-5 = steering map) |
| D1   | Torque A                                          |
| D2   | Torque B                                          |
| D3   | Not used                                          |
| D4   | Not used                                          |
| D5   | Not used                                          |
| D6   | Not used                                          |
| D7   | Not used                                          |

#### Example

Turn *slowly* to the right with: MAP between 1-5 (higher is faster), torque A = 143, torque B = 112.

Message: `01 8F 70 00 00 00 00 00 `

##### Rules

$Torque_A + Torque_B = 255$

