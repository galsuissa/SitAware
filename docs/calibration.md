# Calibration

Sensor readings measured on the real chair, used to choose the detection thresholds.

Values are raw `analogRead()` readings (0–1023), captured in the Arduino IDE Serial Monitor at about 10 readings per second, holding each position for about 10 seconds.

## Sensor mounting

| Sensor | Location |
|---|---|
| Seat FSR (A0) | Under the seat cushion, where body weight rests |
| Backrest FSR (A1) | Directly on the mesh backrest, where the lower back touches it |

**Lesson learned:** the backrest sensor was first placed between the lumbar cushion and the mesh. The cushion pressed on it constantly, so the empty chair read about 500 instead of 0, slowly rising from 212 as the sensor settled (FSR "creep" under constant load). Moving the sensor directly onto the mesh fixed it: the empty chair now reads 0.

## Measurements

| Position | seat | back | State |
|---|---|---|---|
| Empty chair | 0 | 0 | Empty |
| Sitting, leaning back | 1014–1016 | 1016–1018 | Supported |
| Sitting, leaning back very lightly | 1015–1017 | 831–868 | Supported |
| Sitting, leaning forward | 1015–1018 | 0 | **Unsupported** |

## Observations

- **Clean baseline:** with no pressure, both sensors read exactly 0.
- **Very sensitive to first contact:** even a light touch pushes the value above 800. After that, more pressure barely changes it (the sensor saturates near 1023).
- **Large gap between states:** "not touching" is 0, "touching" is above ~830. There are almost no values in between.
- **Short transitional values:** in-between readings (e.g. 212, 598) appear only briefly while moving. They will be handled by the state logic, not by the thresholds.

## Thresholds

| Constant | Value | Gap in the data |
|---|---|---|
| `SEAT_THRESHOLD` | 500 | 0 … 1014 |
| `BACK_THRESHOLD` | 400 | 0 … 831 |

**Why these values:** each threshold sits roughly in the middle of the gap between the "no pressure" and "pressure" groups, leaving a large safety margin on both sides.

- A threshold close to 0 would be crossed by noise or small unintended pressure.
- A threshold close to 1023 would be missed by normal variation. For example, `back > 1000` would treat a light lean (~850) as "no support" and cause false alerts.

These values should be re-checked if the sensors are moved or a different chair is used.
