#pragma once
#include "MotorDC.h"
#include "CambienmauTCS3200.h"
#include "DieukhienServo.h"

const int OUT_FC51 = 13;
int checkstage = 0;

void setupFC51(){
  pinMode(OUT_FC51,INPUT);
  digitalWrite(OUT_FC51, HIGH); //Low active for FC51
}

void openFC51(){
  int stage = digitalRead(OUT_FC51);
  if(stage == LOW){
    Serial.println("Co vat can!!");
    bangtaidunglai();
    delay(300);
    checkstage = openTCS3200();
    if(checkstage > 0){
      executeRobotaim(checkstage);
    }
    else Serial.println("Khong nhan dien duoc mau!!");
  }
  else if (stage == HIGH) {
    Serial.println("Khong co vat can!!");
    bangtaichaytoi();
  }
  delay(100);
}

