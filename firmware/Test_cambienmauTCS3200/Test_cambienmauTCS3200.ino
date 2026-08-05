#define OUT_lg 14
#define S3_lg 25
#define S2_lg 26
#define S1_lg 32
#define S0_lg 33

int redvalue = 0;
int bluevalue = 0;
int greenvalue = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(OUT_lg, INPUT);
  pinMode(S3_lg, OUTPUT);
  pinMode(S2_lg, OUTPUT);
  pinMode(S1_lg, OUTPUT);
  pinMode(S0_lg, OUTPUT);

  digitalWrite(S0_lg, HIGH);  // luôn set là High và Low để có mức 20% (tỷ lệ tần số)
  digitalWrite(S1_lg, LOW);

}

void loop() {
  // put your main code here, to run repeatedly:
  // đo tần số màu đỏ
  digitalWrite(S2_lg, LOW);
  digitalWrite(S3_lg, LOW);
  redvalue = pulseIn(OUT_lg, LOW);
  delay(10);

  // đo tần só màu xanh lá
  digitalWrite(S2_lg, HIGH);
  digitalWrite(S3_lg, HIGH);
  greenvalue = pulseIn(OUT_lg, LOW);
  delay(10);

  // đo tần số màu xanh biển
  digitalWrite(S2_lg, LOW);
  digitalWrite(S3_lg, HIGH);
  bluevalue = pulseIn(OUT_lg, LOW);
  delay(10);

  Serial.print("Mau do la: ");
  Serial.print(redvalue);
  Serial.print(" Mau xanh la: ");
  Serial.print(greenvalue);
  Serial.print(" Mau xanh bien la: ");
  Serial.println(bluevalue);

  delay(500);

  //// đo khoảng cách cố định + code conditions print màu phía sau là được
}
