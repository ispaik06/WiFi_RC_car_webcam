#!/home/ispaik/Desktop/WebpageTestFinal/env/bin python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)  # Disable GPIO warnings

# Motor state definitions
STOP = 0
FORWARD = 1
BACKWARD = 2

# Motor channel definitions
CH1 = 0
CH2 = 1

# Pin mode definitions
OUTPUT = 1
INPUT = 0

# Pin state definitions
HIGH = 1
LOW = 0

# Motor driver pin assignments
ENA = 26
ENB = 16
IN1 = 19
IN2 = 13
IN3 = 6
IN4 = 5

spd = 100  # Default speed for motors (%)

# GPIO pin setup function
def set_pin_config():
    GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

    pwm_a = GPIO.PWM(ENA, 100)  # Create PWM instance for motor A with 100Hz frequency
    pwm_b = GPIO.PWM(ENB, 100)  # Create PWM instance for motor B with 100Hz frequency
    pwm_a.start(0)  # Start PWM with 0% duty cycle
    pwm_b.start(0)  # Start PWM with 0% duty cycle
    return pwm_a, pwm_b

# Motor control function
def control_motor(pwm, INA, INB, speed, state):
    pwm.ChangeDutyCycle(speed)  # Set motor speed

    if state == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
    elif state == BACKWARD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
    elif state == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)

# Direction control function
def control_direction(ch, speed, state):
    if ch == CH1:
        control_motor(pwm_a, IN1, IN2, speed, state)
    elif ch == CH2:
        control_motor(pwm_b, IN3, IN4, speed, state)


def forward(speed):
    control_direction(CH1, speed, FORWARD)
    control_direction(CH2, speed, FORWARD)

def backward(speed):
    control_direction(CH1, speed, BACKWARD)
    control_direction(CH2, speed, BACKWARD)

def right_turn(speed):
    control_direction(CH1, speed, BACKWARD)
    control_direction(CH2, speed, FORWARD)

def left_turn(speed):
    control_direction(CH1, speed, FORWARD)
    control_direction(CH2, speed, BACKWARD)

def go_right(speed):
    control_direction(CH1, speed, STOP)
    control_direction(CH2, speed, FORWARD)

def go_left(speed):
    control_direction(CH1, speed, FORWARD)
    control_direction(CH2, speed, STOP)

def back_right(speed):
    control_direction(CH1, speed, STOP)
    control_direction(CH2, speed, BACKWARD)

def back_left(speed):
    control_direction(CH1, speed, BACKWARD)
    control_direction(CH2, speed, STOP)

def stop():
    control_direction(CH1, 0, STOP)
    control_direction(CH2, 0, STOP)

# GPIO pin setup
pwm_a, pwm_b = set_pin_config()

if __name__ == '__main__':
    forward(spd)
    time.sleep(2)
    backward(spd)
    time.sleep(2)
    left_turn(spd)
    time.sleep(2)
    right_turn(spd)
    time.sleep(2)
    stop()
    GPIO.cleanup()
