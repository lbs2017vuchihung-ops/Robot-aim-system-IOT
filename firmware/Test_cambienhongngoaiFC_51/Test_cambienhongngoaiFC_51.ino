#define OUT_lg 14

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(OUT_lg, INPUT);
  digitalWrite(OUT_lg, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  int stage = digitalRead(OUT_lg);
  if(stage == LOW){
    Serial.println("Co vat can!!");
  }
  else Serial.println("Khong co vat can!!");

  delay(100);
}
