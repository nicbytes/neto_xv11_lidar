const int motorPin = 10;
int speed = 0;
long timer = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("alive");
  analogWrite(motorPin, 0);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '+') {
      speed++;
      if (speed >= 256) speed = 255;
    } else if (c == '-') {
      speed--;
      if (speed < 0) speed = 0;
    } else {
      // ignore other commands for now
    }
  }

  // every three seconds, print speed variable
  if (millis() - timer >= 3 * 1000) {
    timer = millis(); // reset the timer
    Serial.println(speed);
  }

  // update the speed
  analogWrite(motorPin, speed);
}
