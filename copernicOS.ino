/*
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

Maintainer: Jai Peris, Daniel Vayman, Will Heitman

Real-time operating script for CircuitPython-based microcontrollers

See readme for more information.
*/

#include <Adafruit_NeoPixel.h>
#include <time.h>
#include <string.h>

#define NEOPIXEL_PIN 88
#define NEOPIXEL_COUNT 1

// intialize neopixel
Adafruit_NeoPixel led = Adafruit_NeoPixel(NEOPIXEL_COUNT, NEOPIXEL_PIN, NEO_GRB);

// set I/O pins
int APS_OUTPUT = A0;
int APS_INPUT = A2;

// Current version
String VERSION = "1.0";

// set serial timeout, in milliseconds
unsigned long SERIAL_TIMEOUT = 1000;

// throttle input timeout, in milliseconds
int THROTTLE_INPUT_TIMEOUT = 500;
long int last_throttle_input_time = -1.0;

// control variables
float target_throttle = 0.0;

String command = "";

// enum used for system status
enum SystemStatus
{ IDLE, ACTIVE, WARN, FAULTY };

SystemStatus status = IDLE; // Set default system status

void setLed()
{
  if (status == IDLE)
    led.setPixelColor(0, led.Color(0, 255, 255)); // CYAN
  else if (status == FAULTY)
    led.setPixelColor(0, led.Color(255, 0, 0)); // RED
  else if (status == ACTIVE)
    led.setPixelColor(0, led.Color(0, 255, 0)); // GREEN
  else if (status == WARN)
    led.setPixelColor(0, led.Color(255, 200, 0)); // YELLOW

  led.show();

  return;
}

/**
 * @brief Checks for serial input and sets target throttle
 */
void checkForInput()
{
  while(Serial.available() > 0)
  {
    char c = Serial.read(); //read a single character from the buffer

    if(c == 's') { command = ""; } // reset the command if it's the start of a new one
    else if (c == 'e' && Serial.available() == 0) break; // break if it's the end of the buffer
    else { command += c; } // append the voltage character to the command

    last_throttle_input_time = millis(); // update last input time
  }

  target_throttle = command.toFloat(); // set targe throttle to most recent command set in the buffer

  return;
}

/**
 * @brief Sets voltage lines to emulate throttle pedal
 *
 * @param throttle_value (float): Between 0.0-1.0
 *
 */
void setThrottle()
{
  // Compare current time with time last input was received.
  int dt = millis() - last_throttle_input_time;

  if(dt > THROTTLE_INPUT_TIMEOUT)
  {
    Serial.println("Timing out.");
    target_throttle = 0.0;
    status = IDLE;
    setVoltage();
  }
  else
  {
    status = ACTIVE;
    //Serial.println("Throttle: " + String(target_throttle));
    setVoltage();
  }

  return;
}

/**
 * @brief Set base voltage for output
 * Pretty much spits out whatever voltage it's getting from the pedal
 */
void setVoltage()
{
  int base = analogRead(APS_INPUT);

  float input_voltage = base/1024.0*3.3;
  
  // 1.5 and 3.2 are the slopes of the linear regression lines for the APS
  float output = 3.2 * target_throttle + input_voltage;
  
  // Vref for the GCM4 is 3.3, ADC resolution is 12 bits (4096)
  analogWrite(APS_OUTPUT, min(int(output / 3.3 * 4095), 4095)); // convert output to 8-bit PWM

  //Serial.println("Throttle: " + String(target_throttle) + ", Voltage: " + String(input_voltage));
}

/**
 * @brief Driver function that calls the 3 main functions
 */
void spin()
{
  setLed();
  checkForInput();
  setThrottle();
}

/**
 * @brief Ardunio setup function that initializes all variables and I/O
 */
void setup()
{
  target_throttle = 0.0;
  
  static int start = millis();

  // Sets up serial baud rate
  Serial.begin(115200);
  while(!Serial)
  {
    Serial.print("Waiting for serial connection... ");
    Serial.print((millis() - start) / 1000.0);
    Serial.println("s elapsed.");
  }
  Serial.println("Serial connected!\n");

  // Print header
  Serial.println("==         CopernicOS v" + VERSION + "         ==");
  Serial.println("~~ Nova at UTD - nova-utd.github.io ~~\n");

  // set I/O
  pinMode(APS_OUTPUT, OUTPUT);
  pinMode(APS_INPUT, INPUT);

  // set serial timeout, 1 second
  Serial.setTimeout(SERIAL_TIMEOUT);

  // set base voltage 
  setVoltage();

  // set up neopixel
  led.begin();
  led.setBrightness(255);
  status = IDLE;
  setLed();
}

void loop()
{
  spin();
}
