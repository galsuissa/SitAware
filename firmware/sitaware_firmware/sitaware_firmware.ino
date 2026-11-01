// SitAware - detect the sitting state and alert after prolonged unsupported sitting

const int SEAT_PIN = A0;   // seat FSR: detects if someone is sitting
const int BACK_PIN = A1;   // backrest FSR: detects leaning back

const unsigned long ALERT_DELAY_MS = 30000;  // alert after 30 seconds without back support

// The three possible states of the chair
enum SittingState {
  NOT_SITTING,           // 0 - nobody on the chair
  SITTING_NOT_LEANING,   // 1 - only the seat sensor has a value
  SITTING_LEANING        // 2 - both sensors have a value
};

bool timerRunning = false;      // flag: are we currently counting time in state 1?
unsigned long timerStart = 0;   // the millis() value when state 1 began
bool alertActive = false;       // is the alert currently on?

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

  if (state == SITTING_NOT_LEANING) {
    if (!timerRunning) {            // we just entered state 1: start counting
      timerRunning = true;
      timerStart = millis();
    }
    if (!alertActive && millis() - timerStart >= ALERT_DELAY_MS) {
      alertActive = true;           // state 1 has lasted long enough
      Serial.println("*** ALERT: Please sit right and lean back against the backrest! ***");
    }
  } else {                          // leaned back or got up: reset everything
    if (alertActive) {
      Serial.println("*** Good, you are sitting right again. ***");
    }
    timerRunning = false;
    alertActive = false;
  }

  // e.g. seat:1015,back:0,state:1,alert:0
  Serial.print("seat:");
  Serial.print(seatValue);
  Serial.print(",back:");
  Serial.print(backValue);
  Serial.print(",state:");
  Serial.print(state);
  Serial.print(",alert:");
  Serial.println(alertActive);

  delay(100);
}
