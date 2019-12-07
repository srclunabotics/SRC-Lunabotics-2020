/*
  # This Sample code is to test the Digital Servo Shield.
  # Editor : Leff, original by YouYou@DFRobot(Version1.0)
  # Date   : 2016-1-19
  # Ver    : 1.1
  # Product: Digital Servo Shield for Arduino
  # Hardwares:
  1. Arduino UNO
  2. Digital Servo Shield for Arduino
  3. Digital Servos( Compatible with AX-12,CDS55xx...etc)
  4. Power supply:6.5 - 12V
  # How to use:
  If you don't know your Servo ID number, please
  1. Open the serial monitor, and choose NewLine,115200
  2. Send command:'d',when it's finished, please close the monitor and re-open it
  3. Send the command according to the function //controlServo()//
*/

#include <SPI.h>
#include "ServoCds55.h"
ServoCds55 myservo;
char inChar = 0;
int Dig_Num3 = 11;
int Dig_Num2 = 15;
int Dig_Num = 5;
int reverse = 1; //set to -1 to reverse motor controls quickly

const int buttonPin1 = 7;     // the number of the pushbutton pin
const int buttonPin2 = 8;
const int buttonPin3 = 3;
const int buttonPin4 = 4;
int buttonState1 = 0;
int buttonState2 = 0;
int buttonState3 = 0;
int buttonState4 = 0;
bool event = true;


char inputCommand ;         // a string to hold "s" command
boolean inputComplete = false;

void setup () {
  Serial.begin (115200);
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin3, INPUT);
  pinMode(buttonPin4, INPUT);
  myservo.begin ();

}

void loop () {
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  buttonState4 = digitalRead(buttonPin4);
  Serial.print(buttonState1);
  Serial.print(buttonState2);
  Serial.print(buttonState3);
  Serial.println(buttonState4);
  if (event) {
    if (buttonState1 == HIGH && buttonState2 == LOW)
    {
      myservo.rotate(Dig_Num, -35);
    }
    else if (buttonState1 == LOW && buttonState2 == HIGH)
    {
      myservo.rotate(Dig_Num, 60);
    }
    else {
      myservo.rotate(Dig_Num, 0);
    }
    if (buttonState3 == HIGH && buttonState4 == LOW)
    {
      myservo.rotate(Dig_Num2, 75);
    }
    else if (buttonState3 == LOW && buttonState4 == HIGH)
    {
      myservo.rotate(Dig_Num2, -75);
    }
    else {
      myservo.rotate(Dig_Num2, 0);
    }
  }
  else {
    if (buttonState1 == HIGH && buttonState2 == LOW)
    {
      myservo.rotate(Dig_Num3, -200);
    }
    else if (buttonState1 == LOW && buttonState2 == HIGH)
    {
      myservo.rotate(Dig_Num3, 200);
    }
    else {
      myservo.rotate(Dig_Num3, 0);
    }
    if (buttonState3 == HIGH && buttonState4 == LOW)
    {
      myservo.rotate(Dig_Num2, 75);
    }
    else if (buttonState3 == LOW && buttonState4 == HIGH)
    {
      myservo.rotate(Dig_Num2, -75);
    }
    else {
      myservo.rotate(Dig_Num2, 0);
    }
  }

  serialEvent();
  if (inputComplete) {
    Serial.print("Your command is: "); Serial.println(inputCommand); Serial.println("");
    controlServo(inputCommand);
    // clear the command:
    inputCommand = 0;
    inputComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      inputComplete = true;
      break;
    }
    inputCommand += inChar;
  }
}

void controlServo(char val) {
  switch (val) {
    case 's':
      if (event) {
        event = false;
      }
      else {
        event = true;
      }

      break;

    default:
      Serial.println("Only takes command s");

  }
}
