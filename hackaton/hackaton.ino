int fSpeedPin = 5;
int fmotor1APin = 6;
int fmotor2APin = 7;
int fspeed_value_motor1 = 255;

int bSpeedPin = 8;
int bmotor1APin = 9;
int bmotor2APin = 10;
int bspeed_value_motor2 = 255;

int sonarOut = 12;
int sonarIn = 13;

char ch;
char command[3] = {'f', 's', 'm'};

void setup() {
  pinMode(fSpeedPin, OUTPUT);
  pinMode(fmotor1APin, OUTPUT);
  pinMode(fmotor2APin, OUTPUT);
  
  pinMode(bSpeedPin, OUTPUT);
  pinMode(bmotor1APin, OUTPUT);
  pinMode(bmotor2APin, OUTPUT);
  
  pinMode(sonarOut, OUTPUT);
  pinMode(sonarIn, INPUT);
  
  Serial.begin(9600);
}

void loop() {
  ch = Serial.read();
  
  switch(ch) {
    case 'l':
    case 'r':
    case 'f':
      command[0] = ch;
      break;
    case 'g':
    case 's':
    case 'b':
      command[1] = ch;
      command[2] = 'm';
      break;
    case 'a':
    case 'm':
      command[2] = ch;
  }
  
  if(command[0] == 'r') {
    frontMotorRight();
    Serial.println("r");
  } else if(command[0] == 'l') {
    frontMotorLeft();
  } else {
    frontMotorFront();
  }
  
  if(command[0] == 'r' && command[1] == 's') {
    frontMotorLeft();
    backMotorBack();
  } else if(command[0] == 'l' && command[1] == 's') {
    frontMotorRight();
    backMotorBack();
  }
  
  if(command[1] == 'g' && command[2] != 'a') {
    backMotorGo();
    command[2] = 'm';
  } else if(command[1] == 's' && command[2] != 'a') {
    backMotorStop();
    command[2] = 'm';
  } else if(command[1] == 'b' && command[2] != 'a') {
    backMotorBack();
    command[2] = 'm';
  }
  
  if(command[2] == 'a') {
    sonarSensor();
  }
  
  analogWrite(fSpeedPin, fspeed_value_motor1);
  analogWrite(bSpeedPin, bspeed_value_motor2);
  delay(100);
}

void backMotorGo() {
  digitalWrite(bmotor1APin, LOW);
  digitalWrite(bmotor2APin, HIGH);
}

void backMotorStop() {
  digitalWrite(bmotor1APin, LOW);
  digitalWrite(bmotor2APin, LOW);
}

void backMotorBack() {
  digitalWrite(bmotor1APin, HIGH);
  digitalWrite(bmotor2APin, LOW);
}

void frontMotorLeft() {
  digitalWrite(fmotor1APin, HIGH);
  digitalWrite(fmotor2APin, LOW);
}

void frontMotorRight() {
  digitalWrite(fmotor1APin, LOW);
  digitalWrite(fmotor2APin, HIGH);
}

void frontMotorFront() {
  digitalWrite(fmotor1APin, LOW);
  digitalWrite(fmotor2APin, LOW);
}

void sonarSensor() {
  digitalWrite(sonarOut, HIGH);
  delayMicroseconds(10);
  digitalWrite(sonarOut, LOW);
  unsigned long pulseTime = pulseIn(sonarIn, HIGH);
  int distance = pulseTime/58;
  
  Serial.println(distance);
  
  if(distance < 70 && distance >= 40) {
    command[1] = 's';
    backMotorStop();
  } else if(distance < 40) {
    command[1] = 'b';
    backMotorBack();
    if(command[0] == 'r') {
      command[0] = 'l';
      frontMotorLeft();
    } else if(command[0] == 'l') {
      command[0] = 'r';
      frontMotorRight();
    }
  } /*else if (distance > 4000) {
    command[1] = 's';
    backMotorStop();
  } */else {
    command[1] = 'g';
    backMotorGo();
  }
}
