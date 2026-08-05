#include "MotorDC.h"
#include "CambienFC51.h"
#include "CambienmauTCS3200.h"
#include "DieukhienServo.h"

///////// Wifi ////////////
#include <WiFi.h>        //  
#include <HTTPClient.h>  //
///////////////////////////

unsigned long thoiGianPingCuoi = 0;
String pingURL = "http://192.168.100.100:8080/api/ping"; // Đảm bảo IP trùng với IP máy tính bạn  

// ==============================================================================
// 1.Nhập tên và mật khẩu Wi-Fi nhà
// (Lưu ý: Máy tính chạy code Python và ESP32 phải bắt CHUNG 1 mạng Wi-Fi này)
// ==============================================================================
const char* ssid = "Wifi";
const char* password = "MKWifi";

// ==============================================================
// 2.Thay chữ 192.168.x.x thành IP máy tính
// (Tuyệt đối giữ nguyên phần ":8080/api/sensor" ở đuôi)
// ==============================================================
String serverName = "http://192.168.x.x:8080/api/sensor";

// =========================================================
// HÀM GỬI DỮ LIỆU LÊN WEB (Có Tự Động Kết Nối Lại Wi-Fi)
// =========================================================
void sendDataToWeb(String tenMau, String maMau, int r, int g, int b) {
  // 1. KIỂM TRA MẠNG TRƯỚC KHI GỬI
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("CẢNH BÁO: Rớt mạng do Servo kéo dòng! Đang kết nối lại...");
    WiFi.disconnect();
    WiFi.reconnect();
    
    // Đợi tối đa 5 giây để Wi-Fi kết nối lại
    int timeout = 0;
    while (WiFi.status() != WL_CONNECTED && timeout < 10) {
      delay(500);
      Serial.print(".");
      timeout++;
    }
    Serial.println();
  }

  // 2. NẾU MẠNG ĐÃ ỔN ĐỊNH THÌ BẮN DỮ LIỆU
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName); 
    http.addHeader("Content-Type", "application/json"); 
    
    String jsonPayload = "{\"color_name\":\"" + tenMau + "\", \"color_key\":\"" + maMau + "\", \"r\":" + String(r) + ", \"g\":" + String(g) + ", \"b\":" + String(b) + "}";
    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
      Serial.print("-> ĐÃ GỬI WEB MÀU: ");
      Serial.print(tenMau);
      Serial.print(" (Mã: ");
      Serial.print(httpResponseCode);
      Serial.println(")");
    } else {
      Serial.print("-> LỖI GỬI WEB! Mã lỗi: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("-> BÓ TAY: KHÔNG CÓ WI-FI ĐỂ GỬI! Vui lòng kiểm tra lại nguồn điện.");
  }
}

void setup() {  
  Serial.begin(115200);
  delay(1000);

  ///////////////////// Wifi ///////////////////////
  // Bắt đầu kết nối Wi-Fi
  Serial.println();
  Serial.print("Dang ket noi den Wi-Fi: ");
  Serial.println(ssid);
  
  // ÉP ESP32 VÀO CHẾ ĐỘ THU SÓNG (STATION)
  WiFi.mode(WIFI_STA);
  // Ngắt các kết nối cũ bị kẹt (nếu có) trước khi kết nối mới
  WiFi.disconnect(); 
  delay(100);

  WiFi.begin(ssid, password);
  WiFi.setAutoReconnect(true); // Bật chế độ tự động kết nối lại của ESP32
  
  // Chờ cho đến khi kết nối thành công
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("-> Ket noi Wi-Fi THANH CONG!");
  Serial.print("IP cua ESP32: ");
  Serial.println(WiFi.localIP());
  ///////////////////////////////////////////////////

  ///////////////// Moto_DC ////////////////////
  setupMotorDC();
  Serial.println("Set up DC successfully!!");
  //////////////////////////////////////////////

  /////////////// CambienFC51 ///////////////////
  setupFC51();
  Serial.println("Set up FC51 successfully!!");
  ///////////////////////////////////////////////

  ////////////// CambienmauTCS3200 ////////////////
  setupTCS3200();
  Serial.println("Set up FCS3200 successfully!!");
  //////////////////////////////////////////////////

  //////////////////// Servo ///////////////////////
  setupServo();
  Serial.println("Set up Servo successfully!!");
  //////////////////////////////////////////////////

}

void loop() {
  openFC51();
  delay(200);

// --- TÍNH NĂNG NHÁ MÁY (Ping) MỖI 3 GIÂY ---
  if (millis() - thoiGianPingCuoi > 3000) {
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(pingURL);
      
      int httpResponseCode = http.GET(); // Gửi Ping và nhận mã kết quả
      
      Serial.print("-> Đang Ping tới Web... Mã kết quả: ");
      Serial.println(httpResponseCode);
      
      http.end();
    } else {
      // NẾU RỚT MẠNG -> ÉP NÓ KẾT NỐI LẠI NGAY LẬP TỨC
      Serial.println("-> LỖI: Rớt mạng Wi-Fi! Đang tự động kết nối lại...");
      WiFi.disconnect();
      WiFi.reconnect(); 
    }
    thoiGianPingCuoi = millis();
  }

}