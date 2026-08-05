#pragma once
#include <Arduino.h> // Bắt buộc phải có thư viện này để nó hiểu kiểu dữ liệu String

// ==============================================================================
// KHAI BÁO EXTERN: Báo cho file này biết hàm này đang nằm bên file .ino chính
// ==============================================================================
extern void sendDataToWeb(String tenMau, String maMau, int r, int g, int b);

const int S0_lg = 32;
const int S1_lg = 14;
const int S2_lg = 27;
const int S3_lg = 26;
const int OUT_lg = 25;
int stageRED = 0;
int stageGREEN = 0;
int stageBLUE = 0;

void setupTCS3200() {
  //Serial.begin(115200);
  pinMode(S0_lg, OUTPUT);
  pinMode(S1_lg, OUTPUT);
  pinMode(S2_lg, OUTPUT);
  pinMode(S3_lg, OUTPUT);
  pinMode(OUT_lg, INPUT);

  digitalWrite(S0_lg, HIGH);
  digitalWrite(S1_lg, LOW); // Tan so 20% (higher performance)  
}

int openTCS3200(){
  // RED (LOW, LOW)
  digitalWrite(S2_lg, LOW);
  digitalWrite(S3_lg, LOW);
  stageRED = pulseIn(OUT_lg, LOW); // doc xung tai LOW cua OUT
  delay(200);

  // GREEN (HIGH, HIGH)
  digitalWrite(S2_lg, HIGH);
  digitalWrite(S3_lg, HIGH);
  stageGREEN = pulseIn(OUT_lg, LOW);
  delay(200);

  // BLUE (LOW, HIGH)
  digitalWrite(S2_lg, LOW);
  digitalWrite(S3_lg, HIGH);
  stageBLUE = pulseIn(OUT_lg, LOW);
  delay(200);

  // print data
  Serial.print("Data mau do la: ");
  Serial.println(stageRED);
  Serial.print("Data mau xanh la la: ");
  Serial.println(stageGREEN);
  Serial.print("Data mau xanh bien la: ");
  Serial.println(stageBLUE);

  // data phan loai mau
  if (stageRED > 0 && stageRED < 400) { 
      if (stageRED < stageGREEN && stageRED < stageBLUE) {
          Serial.println("======> PHAN LOAI: VAT MAU DO! <======");
          // GỌI HÀM GỬI LÊN WEB TẠI ĐÂY
          sendDataToWeb("ĐỎ", "red", 240, 20, 20); 
          return 1;
      } 
      else {
          float tyLe = (float)stageGREEN / (float)stageBLUE;
          Serial.print("Ty le G/B la: "); 
          Serial.println(tyLe);
          
          if (tyLe > 1.20) {
              Serial.println("======> PHAN LOAI: VAT MAU XANH BIEN! <======");
              // GỌI HÀM GỬI LÊN WEB TẠI ĐÂY
              sendDataToWeb("XANH DƯƠNG", "blue", 15, 30, 230); 
              return 2;
          } 
          else {
              Serial.println("======> PHAN LOAI: VAT MAU XANH LA! <======");
              // GỌI HÀM GỬI LÊN WEB TẠI ĐÂY
              sendDataToWeb("XANH LÁ", "green", 20, 240, 30); 
              return 3;
          }
      }
    }
  return 0;
}