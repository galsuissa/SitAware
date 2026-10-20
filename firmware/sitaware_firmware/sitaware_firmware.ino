// SitAware - Milestone 1: read one FSR and print its value

const int SEAT_PIN = A0;   // the pin the seat FSR is connected to

void setup() {
  Serial.begin(9600);      // start serial communication with the computer
}

void loop() {
  int seatValue = analogRead(SEAT_PIN);   // read the voltage as a number 0-1023

  Serial.println(seatValue);              // send the number to the Serial Monitor

  delay(100);                             // wait 100 ms (about 10 readings per second)
}
