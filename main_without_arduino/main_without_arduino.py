import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, request

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
ENA = 26  # Pin 37
ENB = 16  # Pin 36
IN1 = 19  # Pin 35
IN2 = 13  # Pin 33
IN3 = 6   # Pin 31
IN4 = 5   # Pin 29

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

# Servo motor pin assignments
servo1Pin = 17
servo2Pin = 27
SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3

# Initial angle settings
angle1 = 90
angle2 = 90

GPIO.setup(servo1Pin, GPIO.OUT)
GPIO.setup(servo2Pin, GPIO.OUT)
servo1 = GPIO.PWM(servo1Pin, 50)
servo2 = GPIO.PWM(servo2Pin, 50)
duty1 = SERVO_MIN_DUTY + (angle1 * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
duty2 = SERVO_MIN_DUTY + (angle2 * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
servo1.start(duty1)
servo2.start(duty2)

# Servo motor control functions
def setServo1Pos(degree):
    duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
    servo1.ChangeDutyCycle(duty)

def setServo2Pos(degree):
    duty = SERVO_MIN_DUTY + (degree * (SERVO_MAX_DUTY - SERVO_MIN_DUTY) / 180.0)
    servo2.ChangeDutyCycle(duty)

def constrain(angle):
    if angle >= 180:
        angle = 180
    elif angle <= 0:
        angle = 0
    return angle

# Flask setup
app = Flask(__name__)

current_direction = None
current_speed = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global current_direction, current_speed
    global angle1, angle2
    global spd
    direction = request.form.get('direction')
    speed = int(request.form.get('speed', 255)) 
    spd = int(speed / 255.0 * 100)
    if direction :
        current_direction = direction
        print(f'Direction: {direction}')

    if speed != current_speed:
        current_speed = speed
        print(f'Speed: {speed}')

    if direction == 'Forward':
        forward(spd)
    elif direction == 'Backward':
        backward(spd)
    elif direction == 'Turn left':
        left_turn(spd)
    elif direction == 'Turn right':
        right_turn(spd)
    elif direction == 'Servo up':
        angle1 += 5
        angle1 = constrain(angle1)
        setServo1Pos(angle1)
    elif direction == 'Servo down':
        angle1 -= 5
        angle1 = constrain(angle1)
        setServo1Pos(angle1)
    elif direction == 'Servo turn left':
        angle2 += 5
        angle2 = constrain(angle2)
        setServo2Pos(angle2)
    elif direction == 'Servo turn right':
        angle2 -= 5
        angle2 = constrain(angle2)
        setServo2Pos(angle2)
    elif direction == 'Stop':
        stop()

    return 'OK'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80)
    finally:
        GPIO.cleanup()
