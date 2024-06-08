#!/home/ispaik/Desktop/WebpageTestFinal/env/bin python
import serial
import time

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    timeout=None
)
time.sleep(2)  # 연결이 설정될 때까지 대기
print("시리얼 포트가 성공적으로 열렸습니다.")


while True:
    i = input("입력하세요\n")
    ser.write(i.encode())