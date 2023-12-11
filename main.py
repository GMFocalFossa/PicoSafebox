from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
import machine
import utime
from machine import Pin
from machine import PWM
# Define servo positions for 0 degrees, 90 degrees, 270 degrees
ZERO_DEGREE_PULSE = 1000000  # 1 ms pulse width for 0 degrees
NINETY_DEGREE_PULSE = 1500000  # 1.5 ms pulse width for 90 degrees
TWO_SEVENTY_DEGREE_PULSE = 1750000  # 1.75 ms pulse width for 270 degrees

# Define LED and servo pins
led = Pin(25, Pin.OUT)
servo_pin = Pin(15)

# Initialize PWM for servo control
pwm = PWM(servo_pin)

# Set PWM frequency
pwm.freq(50)
# CONSTANTS
KEY_UP = const(0)
KEY_DOWN = const(1)

keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

# Pin names for Pico
rows = [2, 3, 4, 5]
cols = [6, 7, 8, 9]

# set pins for rows as outputs
row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]

# set pins for cols as inputs
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in cols]

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

code = []

def init():
    for row in range(0, 4):
        for col in range(0, 4):
            row_pins[row].low()


def scan(row, col):
    """ scan the keypad """

    # set the current column to high
    row_pins[row].high()
    key = None

    # check for keypressed events
    if col_pins[col].value() == KEY_DOWN:
        key = KEY_DOWN

    row_pins[row].low()

    # return the key state
    return key


print("starting")

# set all the columns to low
init()

while True:
    for row in range(4):
        for col in range(4):
            key = scan(row, col)
            if key == KEY_DOWN:
                CurrentCode = []
                message = keys[row][col]
                # lcd.putstr(message)
                code.append(message)
                CurrentCode.append(message)
                CurrentCode.append(message)
                CurrentCode.append(message)
                print(CurrentCode)
                if len(code) == 4:
                    print("Added 4 numbers to the list:", code)
                    #code = []
                    if code == ['1', '2', '3', '4']:
                        print("Unlocked!")
                        pwm.duty_ns(TWO_SEVENTY_DEGREE_PULSE)
                        utime.sleep(1)
                        machine.reset()
                    elif code == ['D', 'D', 'D', 'D']:
                        pwm.duty_ns(ZERO_DEGREE_PULSE)
                        utime.sleep(1)
                        machine.reset()
                    else:
                        machine.reset()



    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    # print(I2C_ADDR)
    lcd.blink_cursor_on()

    lcd.putstr("Temp: " + str(temperature))
    lcd.blink_cursor_off()

    sleep(0.1)
    lcd.clear()
