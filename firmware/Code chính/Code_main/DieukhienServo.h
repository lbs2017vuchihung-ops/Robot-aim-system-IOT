#pragma once
#include <ESP32Servo.h>
#include "CambienmauTCS3200.h"

/////// Khởi tạo 4 servo ////////
Servo s1;
Servo s2;
Servo s3;
Servo s4;
Servo s5;
/////////////////////////////////

const int Pin_s1 = 4;
const int Pin_s2 = 19;
const int Pin_s3 = 21;
const int Pin_s4 = 22;
const int Pin_s5 = 23;

const int Home_s1 = 85; // Đế
const int Home_s2 = 165; // Vai
const int Home_s3 = 120; // Khuỷu
const int Home_s4 = 120; // Cổ tay nâng hạ
const int Home_s5 = 110; // kẹp

void setupServo(){
  Serial.begin(115200);

  ////////////////////////////////////////////////////////////
  // Khởi tạo cấu hình Timer + chia tần số xung cho ESP32   //
  // Lý do: Adruino Uno tự chia xung -> ESP32 có 4 luồng    //
  //        chia xung độc lập để tạo xung PWM -> Nếu cho    //
  //        4 servo dùng chung 1 timer -> xảy ra hiện tượng //
  //        bị nhiễu xung -> 1 servo chạy dẫn đến các servo //
  //        khác cũng bị giật theo                          //
  ////////////////////////////////////////////////////////////
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);

  /////////////////////////////////////////////////////////////
  // Ép các servo sử dụng xung 50Hz theo tiêu chuẩn          //
  // Lý do: Chống cháy linh kiện -> Vì có thể tự phát ở xung //
  //        cao hơn 100 or 200Hz                             //
  /////////////////////////////////////////////////////////////
  s1.setPeriodHertz(50);
  s2.setPeriodHertz(50);
  s3.setPeriodHertz(50);
  s4.setPeriodHertz(50);
  s5.setPeriodHertz(50);

  //////////////////////////////////////////////////////////////
  // Lệnh attach(chân) -> bắt buộc, 500 là độ rộng xung tương //
  // với góc 0 độ và 2400 là độ rộng xung tương ứng với góc   //
  // 180 độ                                                   //
  // Lý do: ép servo quay full các góc trong 180 độ -> nếu    //
  //        chỉ để attach bình thường -> có thể quay tối đa   //
  //        chỉ khoảng 100-120 độ                             //
  //////////////////////////////////////////////////////////////
  s1.attach(Pin_s1, 500, 2400);
  s2.attach(Pin_s2, 500, 2400);
  s3.attach(Pin_s3, 500, 2400);
  s4.attach(Pin_s4, 500, 2400);
  s5.attach(Pin_s5, 500, 2400);

  ///////////////////////////////////////////////////////////////
  // Đưa các servo về vị trí ban đầu -> Sử dụng delay 2000 để  //
  // ESP32 đứng im 2s -> để cánh tay quay về vị trí cũ rồi mới //
  // tiếp tục quay                                             //
  ///////////////////////////////////////////////////////////////
  s1.write(Home_s1);
  s2.write(Home_s2);
  s3.write(Home_s3);
  s4.write(Home_s4);
  s5.write(Home_s5);
  delay(2000);
}

////////////////////////////////////////////////////////////////////////
// Hàm giảm giật, rung cho cánh tay khi quay -> Thay vì bắt cánh tay  //
// xoay liền góc đó -> tiến hành băm nhỏ quãng đường thành từng độ    //
// nhỏ để xoay                                                        //
// Lý do: delay time càng lớn -> cành tay xoay càng chậm và ngược lại //                                                        
////////////////////////////////////////////////////////////////////////

/*void reduces1(Servo& myservo, int startAngle, int targetAngle, int delaytime) { // s1: kẹp
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

void reduces2(Servo& myservo, int startAngle, int targetAngle, int delaytime) { // reduce for s2
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

void reduces3(Servo& myservo, int startAngle, int targetAngle, int delaytime) { // reduce for s3
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

void reduces4(Servo& myservo, int startAngle, int targetAngle, int delaytime) { // reduce for s4
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
}*/

/*void reduces5(Servo& myservo, int startAngle, int targetAngle, int delaytime) { // reduce for s5
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
}*/

////////////////////////////////////////////////////////////////////////
// HÀM QUAY SERVO 
////////////////////////////////////////////////////////////////////////
void instantMove(Servo& myservo, int targetAngle, int delaytime) {
  // Bẻ lái cái rụp tới đích luôn!
  myservo.write(targetAngle); 
  
  // LƯU Ý: Vẫn phải có một nhịp nghỉ nhỏ để nhông cốt bên trong Servo kịp xoay tới nơi.
  // Vì các con số delaytime (2, 5, 10) là quá bé so với tốc độ thực tế của Servo,
  // nên nhân thêm hệ số 30 để cánh tay không bị vấp lệnh tiếp theo.
  delay(delaytime * 30); 
}

// ==============================================================
// Gắn tạm các tên hàm cũ vào hàm mới để code bên dưới không bị lỗi
// ==============================================================
void reduces1(Servo& myservo, int startAngle, int targetAngle, int delaytime) { instantMove(myservo, targetAngle, delaytime); }
void reduces2(Servo& myservo, int startAngle, int targetAngle, int delaytime) { instantMove(myservo, targetAngle, delaytime); }
void reduces3(Servo& myservo, int startAngle, int targetAngle, int delaytime) { instantMove(myservo, targetAngle, delaytime); }
void reduces4(Servo& myservo, int startAngle, int targetAngle, int delaytime) { instantMove(myservo, targetAngle, delaytime); }
void reduces5(Servo& myservo, int startAngle, int targetAngle, int delaytime) { instantMove(myservo, targetAngle, delaytime); }

void executeRobotaim(int Outstage){
  // Lưu các giá trị ban đầu của từng khớp
  int curr_s1 = Home_s1; // 0
  int curr_s2 = Home_s2; // 45
  int curr_s3 = Home_s3; // 90
  int curr_s4 = Home_s4; // 90
  int curr_s5 = Home_s5; // 0

  if(Outstage == 1 || Outstage == 2){

    //////////////////////////////
    // Quá trình 1: Tới gắp vật //
    //////////////////////////////
    reduces1(s1, curr_s1, 115, 2); // Xoay qua vị trí gắp
    curr_s1 = 115; 
    delay(100);

    reduces4(s4, curr_s4, 130, 5); // Hạ kẹp xuống 15 độ
    curr_s4 = 130;
    delay(100);

    reduces2(s2, curr_s2, 130, 5); // Hạ vai xuống 35 độ
    curr_s2 = 130;
    delay(100);

    reduces5(s5, curr_s5, 35, 10); // kẹp vật
    curr_s5 = 35;
    delay(100);

    reduces2(s2, curr_s2, 165, 5); // Đưa vai lên 35 độ
    curr_s2 = 165;
    delay(300);

    //////////////////////////////
    // Quá trình 2: Đưa vật đi  //
    //////////////////////////////
    if(Outstage == 1){ // Màu đỏ
      reduces1(s1, curr_s1, 59, 2); // Xoay đế qua 75 độ để vừa với hộp đựng vật màu đỏ
      curr_s1 = 59;
      delay(200);
    }
    else if(Outstage == 2){
      reduces1(s1, curr_s1, 19, 2); // Xoay đế qua 75 độ để vừa với hộp đựng vật màu xanh biển
      curr_s1 = 19;
      delay(200);
    }

    ////////////////////////////////
    // Quá trình 3: Thả vật xuống //
    ////////////////////////////////
    if(Outstage == 1){
      reduces4(s4, curr_s4, 145, 5); // hạ kẹp xuống 15 độ
      curr_s4 = 145;
      delay(200);

      reduces2(s2, curr_s2, 130, 5); // Đưa vai xuống 45 độ
      curr_s2 = 130;
      delay(200);
    }
    else if(Outstage == 2){
      reduces4(s4, curr_s4, 110, 5); // hạ kẹp xuống 15 độ
      curr_s4 = 110;
      delay(200);

      reduces2(s2, curr_s2, 150, 5); // Đưa vai xuống 45 độ
      curr_s2 = 150;
      delay(200);
    }

    reduces5(s5, curr_s5, 110, 10); // Thả vật
    curr_s5 = 110;
    delay(200);

    /////////////////////////////////////////////////
    // Quá trình 4: Đưa cánh tay về vị trì ban đầu //
    /////////////////////////////////////////////////
    reduces2(s2, curr_s2, Home_s2, 5); // Đưa vai về vị trí ban đầu
    curr_s2 = Home_s2;
    delay(100);
    
    reduces1(s1, curr_s1, Home_s1, 2); // Xoay đế về vị trí ban đầu 0 độ
    curr_s1 = Home_s1;
    delay(100);
    

    reduces4(s4, curr_s4, Home_s4, 5); // Đưa nâng hạ kẹp về vị trí ban đầu
    curr_s4 = Home_s4;  
    delay(2000);

    Serial.println("San sang cho vat tiep theo");
    delay(200);
  }
  else if(Outstage == 3){
    //////////////////////////////
    // Quá trình 1: Tới gắp vật //
    //////////////////////////////
    reduces1(s1, curr_s1, 115, 2); // Xoay qua vị trí gắp
    curr_s1 = 115; 
    delay(100);

    reduces4(s4, curr_s4, 130, 5); // Hạ kẹp xuống 15 độ
    curr_s4 = 130;
    delay(100);

    reduces2(s2, curr_s2, 130, 5); // Hạ vai xuống 35 độ
    curr_s2 = 130;
    delay(100);

    reduces5(s5, curr_s5, 45, 10); // kẹp vật
    curr_s5 = 45;
    delay(100);

    reduces2(s2, curr_s2, 165, 5); // Đưa vai lên 35 độ
    curr_s2 = 165;
    delay(300);

    //////////////////////////////
    // Quá trình 2: Đưa vật đi  //
    //////////////////////////////
    reduces1(s1, curr_s1, 40, 2); // Xoay đế qua 75 độ để vừa với hộp đựng vật màu xanh lá
    curr_s1 = 40;
    delay(200);


    ////////////////////////////////
    // Quá trình 3: Thả vật xuống //
    ////////////////////////////////
    reduces4(s4, curr_s4, 100, 5); // hạ kẹp xuống 15 độ
    curr_s4 = 100;
    delay(200);

    reduces2(s2, curr_s2, 150, 5); // Đưa vai xuống 45 độ
    curr_s2 = 150;
    delay(200);

    reduces5(s5, curr_s5, 110, 10); // Thả vật
    curr_s5 = 110;
    delay(200);

    /////////////////////////////////////////////////
    // Quá trình 4: Đưa cánh tay về vị trì ban đầu //
    /////////////////////////////////////////////////
    reduces2(s2, curr_s2, Home_s2, 5); // Đưa vai về vị trí ban đầu
    curr_s2 = Home_s2;
    delay(100);
    
    reduces1(s1, curr_s1, Home_s1, 2); // Xoay đế về vị trí ban đầu 0 độ
    curr_s1 = Home_s1;
    delay(100);
    

    reduces4(s4, curr_s4, Home_s4, 5); // Đưa nâng hạ kẹp về vị trí ban đầu
    curr_s4 = Home_s4;  
    delay(2000);

    Serial.println("San sang cho vat tiep theo");
    delay(200);
  }
}