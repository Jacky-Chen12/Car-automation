#include <Servo.h>
#include <NewPing.h>
#define trigPin1 12
#define echoPin2 13
#define max_distance 250

Servo myservo1;
Servo myservo2;
Servo myservo3;

NewPing sonar1(trigPin1, echoPin2, max_distance);

int distance; int duration;

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, INPUT);
  myservo1.attach(3);
  myservo2.attach(5);
  myservo3.attach(9);

  myservo3.write(90);
  distance = readPing();
  delay(200);

}

void loop() {
  int distanceL = 0;
  int distanceR = 0;
  int distanceA = 0;

  if (distance < 20) 
  {
    moveStop();
    delay(100);
    moveBackward();
    delay(400);
    moveStop();
    delay(100);
    distanceR = lookRight();
    delay(400);
    Serial.print("objectdetected")
    distanceL = lookLeft();
    delay(400);

    if (distanceR <= distanceL) 
    {
      moveRight();
      delay(1000);
      moveStop();
      lookAhead();
    }
    else 
    {
      moveLeft();
      delay(1000);
      moveStop();
      lookAhead();
    }
  }
    else 
    {
      lookAhead();
      moveForward();
    }
      distance = readPing();
  }



int readPing() {
  delay(10);
  int cm = sonar1.ping_cm();
  if (cm == 0) {
    cm = 250;
  }
  return cm;

  }
int lookLeft() {
  myservo3.write(180);
  readPing();
}
int lookAhead() {
  myservo3.write(90);
  readPing();
}
int lookRight() {
  myservo3.write(0);
  readPing();
}

void moveForward() {
  myservo1.write(0);
  myservo2.write(180);
}

void moveBackward() {
  myservo1.write(180);
  myservo2.write(0);
}

void moveRight() {
  myservo1.write(180);
  myservo2.write(180);
}

void moveLeft() {
  myservo1.write(0);
  myservo2.write(0);
}

void moveStop() {
  myservo1.write(90);
  myservo2.write(90);
}
