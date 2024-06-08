#include <Servo.h>

Servo servo1, servo2;

const int servo1Pin = 13;
const int servo2Pin = 33;

int spd = 255;
int angle1 = 90;
int angle2 = 90;

void setup() {
  Serial.begin(9600);
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
  
  servo1.write(angle1);
  servo2.write(angle2);
}


void loop() {
  if(Serial.available()>0) {
    char s = Serial.read();
    Serial.println(s);
    if(s == 'U') {
      angle1+=5;
    }
    else if(s == 'D') {
      angle1-=5;
    }
    else if(s == 'L') {
      angle2+=5;
    }
    else if(s == 'R') {
      angle2-=5;
      
    }
    
    angle1 = constrain(angle1, 0, 180);
    angle2 = constrain(angle2, 0, 180);
    servo1.write(angle1);
    servo2.write(angle2);
    Serial.print(angle1);
    Serial.print(",");
    Serial.println(angle2);
    
  }
}
