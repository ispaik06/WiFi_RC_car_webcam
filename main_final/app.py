#!/home/ispaik/Desktop/WebpageTestFinal/env/bin python
import RPi.GPIO as GPIO
import time
import serial
from flask import Flask, render_template, request, Response
import cv2

GPIO.setwarnings(False)

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

# Backward right function
def back_right(speed):
    control_direction(CH1, speed, STOP)
    control_direction(CH2, speed, BACKWARD)

# Backward left function
def back_left(speed):
    control_direction(CH1, speed, BACKWARD)
    control_direction(CH2, speed, STOP)

# Stop function
def stop():
    control_direction(CH1, 0, STOP)
    control_direction(CH2, 0, STOP)

# GPIO pin setup
pwm_a, pwm_b = set_pin_config()



# 웹캠 캡처를 위한 함수
def gen_frames():  
    camera = cv2.VideoCapture(0)  # 웹캠을 열기
    while True:
        success, frame = camera.read()  # 프레임 읽기
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 프레임 반환



seri = serial.Serial(
    port='/dev/cu.usbmodem11301',
    baudrate=9600,
    timeout=None
)
time.sleep(1)
print("시리얼 포트가 성공적으로 열렸습니다.")

app = Flask(__name__)

current_direction = None
current_speed = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # 스트리밍 응답


@app.route('/move', methods=['POST'])
def move():
    global current_direction, current_speed
    global angle1, angle2
    global spd
    direction = request.form.get('direction')
    speed = int(request.form.get('speed', 255))
    spd = int(speed / 255.0 * 100)
    if direction:
        current_direction = direction
        print(f'Direction: {direction}')
    
    if speed != current_speed:
        current_speed = speed
        print(f'Speed: {speed}')
        
    a = 5
    if direction == 'Forward':
        forward(spd)
    elif direction == 'Backward':
        backward(spd)
    elif direction == 'Turn left':
        left_turn(spd)
    elif direction == 'Turn right':
        right_turn(spd)
    elif direction == 'Servo up':
        c = 'U'
        seri.write(c.encode())
    elif direction == 'Servo down':
        c = 'D'
        seri.write(c.encode())
    elif direction == 'Servo turn left':
        c = 'L'
        seri.write(c.encode())
    elif direction == 'Servo turn right':
        c = 'R'
        seri.write(c.encode())
    elif direction == 'Stop':
        stop()

    return 'OK'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8081)
    finally:
        GPIO.cleanup()
