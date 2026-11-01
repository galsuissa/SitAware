// SitAware - detect the sitting state

const int SEAT_PIN = A0;   // seat FSR: detects if someone is sitting
const int BACK_PIN = A1;   // backrest FSR: detects leaning back

// The three possible states of the chair
enum SittingState {
  NOT_SITTING,           // 0 - nobody on the chair
  SITTING_NOT_LEANING,   // 1 - only the seat sensor has a value
  SITTING_LEANING        // 2 - both sensors have a value
};

void setup() {
  Serial.begin(9600);
}

// Decide the state: a sensor "has a value" when its reading is above 0
SittingState getSittingState(int seatValue, int backValue) {
  if (seatValue > 0 && backValue > 0) {
    return SITTING_LEANING;        // both sensors have values
  }
  if (seatValue > 0) {
    return SITTING_NOT_LEANING;    // only the seat sensor has a value
  }
  return NOT_SITTING;              // seat is 0: nobody is sitting
}

void loop() {
  int seatValue = analogRead(SEAT_PIN);
  int backValue = analogRead(BACK_PIN);

  SittingState state = getSittingState(seatValue, backValue);

  // e.g. seat:1015,back:0,state:1
  Serial.print("seat:");
  Serial.print(seatValue);
  Serial.print(",back:");
  Serial.print(backValue);
  Serial.print(",state:");
  Serial.println(state);

  delay(100);
}
