# CopernicOS

The goal of this script is to manage low-level IO for an autonomous vehicle, including CAN communication, safety checks, and interfaces with the vehicle's stock control module.

All of this should be done in *real time*. This means that every request should be attended to and completed within a guaranteed maximum delay.

To accomplish this, all tasks should be identified and evaluated in a **main loop**. External events should be read in (such as from the high-level onboard computer, the GNSS sensor, the CAN linear actuator, etc). This loop should **r**ead new events, **e**valuate them, **p**rint the results as necessary to the onboard computer, and **l**oop to the beginning. This architecture is called a **REPL**.



## Main loop

```python
while True:
    # Read
    readSerialMessages()
    readBrakeMessages() # Check for error states etc
    readGnssMessages() # In the  future
    
    # Evaluate
    runBrakeCommand()
    runThrottleCommand()
    
    # Print
    sendAck() # Send an acknowledgment to the OBC with summary of actions
```

## Serial command protocol

The general format is:

`$[SEQ],[VERB],[PARAMS]\n`

Of course, `\n` is a newline control character. For the sake of simplicity, **\n will be assumed in the rest of this document**.

### Throttle

`$1,THROTTLE,0.42\n`