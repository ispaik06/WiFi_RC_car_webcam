#include <Servo.h>

// Servo motor setting
Servo servo1, servo2; 

const int servo1Pin = 11;
const int servo2Pin = 9;
int angle1 = 90;
int angle2 = 90;
int a = 10;

// Ultrasonic sensor & LED Pin
const int TRIG = 12;
const int ECHO = 13;
int R = 3;
int G = 5;
int B = 6;
int bu = 8;

void setup() {
  Serial.begin(9600);
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);

  pinMode(TRIG,OUTPUT);  
  pinMode(ECHO,INPUT);
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(bu, INPUT);


  servo1.write(angle1);
  servo2.write(angle2);
}


void loop() {
  // Serial communication 
  if(Serial.available()>0) {
    char s = Serial.read();
    Serial.println(s);
    if(s == 'U') {
      angle1+=a;
    }
    else if(s == 'D') {
      angle1-=a;
    }
    else if(s == 'L') {
      angle2-=a;
    }
    else if(s == 'R') {
      angle2+=a;
    }
    
    angle1 = constrain(angle1, 0, 180);
    angle2 = constrain(angle2, 0, 180);
    servo1.write(angle1);
    servo2.write(angle2);
    Serial.print(angle1);
    Serial.print(",");
    Serial.println(angle2); 
  }

  // LED
  float distance = getDis();
  if (distance<10 && distance>0){
    color(255,0,0);
    tone(bu,392);
  }
  else if (distance<40) {
    int temp = ceil(255*(distance-7)/30);
    color(255-temp,temp,0);
    noTone(bu);
  }
  else {
    color(0,255,0);
    noTone(bu);
  }

}

void color(int Rv, int Gv, int Bv) {
  analogWrite(R,Rv);
  analogWrite(G,Gv);
  analogWrite(B,Bv);
}

float getDis() {
  float duration;
  digitalWrite(TRIG,HIGH);
  delay(10);
  digitalWrite(TRIG,LOW);

  duration = pulseIn(ECHO,HIGH);
  return duration*17/1000;
}
