#pragma once
const int INT1 = 5;
const int INT2 = 18;

void setupMotorDC(){
  pinMode(INT1, OUTPUT);
  pinMode(INT2, OUTPUT);

  digitalWrite(INT1, LOW);
  digitalWrite(INT2, LOW);
}

void bangtaichaytoi(){
  digitalWrite(INT1, HIGH);
  digitalWrite(INT2, LOW);
}

void bangtaichaylui(){
  digitalWrite(INT1, LOW);
  digitalWrite(INT2, HIGH);
}

void bangtaidunglai(){
  digitalWrite(INT1, LOW);
  digitalWrite(INT2, LOW);
}