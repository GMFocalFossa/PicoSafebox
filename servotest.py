from machine import Pin, PWM
import utime

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

while True:
    # Rotate servo to 270 degrees
    pwm.duty_ns(TWO_SEVENTY_DEGREE_PULSE)
    utime.sleep(1)

    # Rotate servo to 0 degrees
    pwm.duty_ns(ZERO_DEGREE_PULSE)
    utime.sleep(1)
