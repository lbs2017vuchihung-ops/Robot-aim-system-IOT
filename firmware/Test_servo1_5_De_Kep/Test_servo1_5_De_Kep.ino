#include <ESP32Servo.h>

Servo s1;
Servo s5;
Servo s2;
Servo s3;
Servo s4;
const int Pin_s1 = 4;
const int Pin_s5 = 23;
const int Pin_s2 = 19;
const int Pin_s3 = 21;
const int Pin_s4 = 22;
const int Home_s2 = 165;
const int Home_s1 = 85;
const int Home_s5 = 110;
const int Home_s3 = 180;
const int Home_s4 = 100;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  s1.setPeriodHertz(50);
  s5.setPeriodHertz(50);
  s2.setPeriodHertz(50);
  s3.setPeriodHertz(50);
  s4.setPeriodHertz(50);
  s1.write(Home_s1);
  s5.write(Home_s5);
  s2.write(Home_s2);
  s3.write(Home_s3);
  s4.write(Home_s4);
  s1.attach(Pin_s1, 500, 2400); 
  s5.attach(Pin_s5, 500, 2400);
  s2.attach(Pin_s2, 500, 2400);
  s3.attach(Pin_s3, 500, 2200);
  s4.attach(Pin_s4, 500, 2400);

  delay(200);
}

/*void reduce(Servo& myservo, int start, int target, int delaytime){
  if(start<target){
    for(int i=start; i<=target; i++){
      myservo.write(i);
      delay(delaytime);
    }
  }
  else if(start>target){
    for(int i=start; i>=target; i--){
      myservo.write(i);
      delay(delaytime);
    }
  }
}*/

void reduces1(Servo& myservo, int startAngle, int targetAngle, int delaytime) { // s1: kẹp
  int start_us = map(startAngle, 0, 180, 500, 2400);
  int target_us = map(targetAngle, 0, 180, 500, 2400);
  int micro_delay = delaytime / 5; 
  if (micro_delay < 1) micro_delay = 1; 
  if (start_us < target_us) {
    for (int i = start_us; i <= target_us; i += 23) { 
      myservo.writeMicroseconds(i);
      delay(micro_delay);
    }
  } 
  else if (start_us > target_us) {
    for (int i = start_us; i >= target_us; i -= 23) {
      myservo.writeMicroseconds(i);
      delay(micro_delay);
    }
  }
  myservo.write(targetAngle); 
}

void reduces5(Servo& myservo, int startAngle, int targetAngle, int delaytime) { // s5: kẹp
  int start_us = map(startAngle, 0, 180, 500, 2400);
  int target_us = map(targetAngle, 0, 180, 500, 2400);
  int micro_delay = delaytime / 5; 
  if (micro_delay < 1) micro_delay = 1; 
  if (start_us < target_us) {
    for (int i = start_us; i <= target_us; i += 20) { 
      myservo.writeMicroseconds(i);
      delay(micro_delay);
    }
  } 
  else if (start_us > target_us) {
    for (int i = start_us; i >= target_us; i -= 20) {
      myservo.writeMicroseconds(i);
      delay(micro_delay);
    }
  }
  myservo.write(targetAngle); 
}

void reduces2(Servo& myservo, int startAngle, int targetAngle, int delaytime) { // s2
  int start_us = map(startAngle, 0, 180, 500, 2400);
  int target_us = map(targetAngle, 0, 180, 500, 2400);
  int micro_delay = delaytime / 5; 
  if (micro_delay < 1) micro_delay = 1; 
  if (start_us < target_us) {
    for (int i = start_us; i <= target_us; i += 23) { 
      myservo.writeMicroseconds(i);
      delay(micro_delay);
    }
  } 
  else if (start_us > target_us) {
    for (int i = start_us; i >= target_us; i -= 23) {
      myservo.writeMicroseconds(i);
      delay(micro_delay);
    }
  }
  myservo.write(targetAngle); 
}

void reduces3(Servo& myservo, int startAngle, int targetAngle, int delaytime) { // s3
  int start_us = map(startAngle, 0, 180, 500, 2200);
  int target_us = map(targetAngle, 0, 180, 500, 2200);
  int micro_delay = delaytime / 5; 
  if (micro_delay < 1) micro_delay = 1; 
  if (start_us < target_us) {
    for (int i = start_us; i <= target_us; i += 10) { 
      myservo.writeMicroseconds(i);
      delay(micro_delay);
    }
  } 
  else if (start_us > target_us) {
    for (int i = start_us; i >= target_us; i -= 10) {
      myservo.writeMicroseconds(i);
      delay(micro_delay);
    }
  }
  myservo.write(targetAngle); 
}

void xoayCoTayCungChieu(int tocDo, int thoiGian) {
  // tocDo: từ 91 đến 180 (gần 180 quay càng nhanh)
  s4.write(tocDo);
  delay(thoiGian); // Quay trong bao lâu (mili-giây)
  s4.write(90);    // 90 là lệnh DỪNG LẠI
}

void xoayCoTayNguocChieu(int tocDo, int thoiGian) {
  // tocDo: từ 0 đến 89 (gần 0 quay càng nhanh)
  s4.write(tocDo);
  delay(thoiGian); // Quay trong bao lâu
  s4.write(90);    // DỪNG LẠI
}
int cur1 = Home_s1;
int cur5 = Home_s5;
int cur2 = Home_s2;
int cur3 = Home_s3;
int cur4 = Home_s4;
void executeaim(){
  /*reduces1(s1, cur1, 115, 5); // s1
  cur1 = 115;
  delay(200);

  reduces2(s2, cur2, 120, 5); // s2
  cur2 = 120;
  delay(200);
  
  reduces5(s5, cur5, 65, 10); // s5
  cur5 = 65;
  delay(200);

  reduces2(s2, cur2, 165, 5); // s2
  cur2 = 165;
  delay(200);

  reduces1(s1, cur1, 59, 5); //s1
  cur1 = 59;
  delay(200);

  reduces2(s2, cur2, 120, 5); // s2
  cur2 = 120;
  delay(200);

  reduces5(s5, cur5, 110, 10); // s5
  cur5 = 110;
  delay(200);

  reduces2(s2, cur2, 165, 5); // s2
  cur2 = 165;
  delay(200);

  reduces1(s1, cur1, 85, 5); //s1
  cur1 = 85;
  delay(3000);*/

  // Xoay cổ tay sang phải một chút (chạy tốc độ chậm 100 trong 500 mili-giây rồi dừng)
  xoayCoTayCungChieu(100, 500);
  delay(2000);

  // Xoay cổ tay ngược lại (chạy tốc độ chậm 80 trong 500 mili-giây rồi dừng)
  xoayCoTayNguocChieu(80, 500);
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  executeaim();
}
