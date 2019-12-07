#include <SPI.h>
#include "ServoCds55.h"
ServoCds55 myservo;

//Use this script to set IDs of motors one at a time.
//Step 1: Set New_servo_ID to desried ID for motor
//Step 2: Plug said motor into the black Arduino shield run command (only one)
//Step 3: Plug in 6-12V into the green power block
//Step 4: upload this file to the arduino. (press reset button on arduino to ensure code runs while motor is on)

int New_servo_ID = 30; //Set all connected motors to this value

void setup () {
  Serial.begin (115200);
  myservo.begin ();
  for (int buf = 0; buf < 255; buf++) {
    myservo.Reset(buf);
    myservo.SetID(1, New_servo_ID);
  }
}

void loop () {

}
