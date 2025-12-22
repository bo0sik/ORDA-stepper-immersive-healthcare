// --- 핀 설정 ---
// 오른쪽 센서 (Right)
#define TRIG_PIN_RIGHT 9
#define ECHO_PIN_RIGHT 10

// 왼쪽 센서 (Left)
#define TRIG_PIN_LEFT 7
#define ECHO_PIN_LEFT 6

// --- 상태 저장 (0 = outside, 1 = inside) ---
int lastStateRight = 0;
int lastStateLeft  = 0;

void setup() {
  Serial.begin(9600);

  pinMode(TRIG_PIN_RIGHT, OUTPUT);
  pinMode(ECHO_PIN_RIGHT, INPUT);
  pinMode(TRIG_PIN_LEFT, OUTPUT);
  pinMode(ECHO_PIN_LEFT, INPUT);
}

void loop() {
  // 오른쪽 거리 측정
  long distanceRight = getDistance(TRIG_PIN_RIGHT, ECHO_PIN_RIGHT);
  int currentStateRight = (distanceRight < 15 && distanceRight > 1) ? 1 : 0;

  // 10cm 안으로 새로 들어온 순간에만 출력
  if (currentStateRight == 1 && lastStateRight == 0) {
    Serial.println("R");
  }
  lastStateRight = currentStateRight;

  delay(50);

  // 왼쪽 거리 측정
  long distanceLeft = getDistance(TRIG_PIN_LEFT, ECHO_PIN_LEFT);
  int currentStateLeft = (distanceLeft < 15 && distanceLeft > 1) ? 1 : 0;

  // 10cm 안으로 새로 들어온 순간에만 출력
  if (currentStateLeft == 1 && lastStateLeft == 0) {
    Serial.println("L");
  }
  lastStateLeft = currentStateLeft;

  delay(50);
}


// 거리 측정 함수
long getDistance(int trigPin, int echoPin) {
  long duration, distance;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH, 30000); // 타임아웃 추가(30ms)
  distance = (duration * 0.034) / 2;

  return distance;
}
