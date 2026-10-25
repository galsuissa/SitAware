// SitAware - Milestone 1: read both FSRs and print their values

const int SEAT_PIN = A0;   // seat FSR: detects if someone is sitting
const int BACK_PIN = A1;   // backrest FSR: detects leaning back

void setup() {
  Serial.begin(9600);      // start serial communication with the computer
}

void loop() {
  int seatValue = analogRead(SEAT_PIN);   // read each sensor as a number 0-1023
  int backValue = analogRead(BACK_PIN);

  // Print one line in "label:value,label:value" format, e.g. seat:512,back:230
  Serial.print("seat:");
  Serial.print(seatValue);
  Serial.print(",back:");
  Serial.println(backValue);              // println ends the line

  delay(100);                             // wait 100 ms (about 10 readings per second)
}
