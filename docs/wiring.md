# Wiring

SitAware uses two FSR (Force Sensitive Resistor) sensors connected to an Arduino Uno R3 through a breadboard.

## Components

| Component | Quantity |
|---|---|
| Arduino Uno R3 | 1 |
| FSR sensor | 2 |
| 10kΩ resistor | 2 |
| Breadboard | 1 |
| Jumper wires | ~6 |
| USB cable (Arduino ↔ computer) | 1 |

## How each sensor is connected

The Arduino cannot measure resistance directly, only voltage. Each FSR is therefore connected in series with a 10kΩ resistor to form a **voltage divider**:

```
5V ──── FSR ────┬──── 10kΩ ──── GND
                │
           Analog pin (A0 / A1)
```

- **No pressure:** the FSR has very high resistance, so the analog pin reads close to **0**.
- **Pressure:** the FSR resistance drops, so the reading rises toward **1023**.

More pressure means a higher reading.

## Connections

### Power

| From | To |
|---|---|
| Arduino 5V | Breadboard + rail |
| Arduino GND | Breadboard − rail |

### FSR 1: seat sensor → A0

| From | To |
|---|---|
| FSR leg 1 | + rail (5V) |
| FSR leg 2 | Breadboard hole a10 |
| 10kΩ resistor | c10 → − rail (GND) |
| Jumper | e10 → Arduino A0 |

### FSR 2: backrest sensor → A1

| From | To |
|---|---|
| FSR leg 1 | + rail (5V) |
| FSR leg 2 | Breadboard hole a20 |
| 10kΩ resistor | c20 → − rail (GND) |
| Jumper | e20 → Arduino A1 |

## Pin summary

| Arduino pin | Purpose |
|---|---|
| A0 | Seat FSR (is someone sitting?) |
| A1 | Backrest FSR (is the user leaning back?) |
| 5V | Power for both sensors (via + rail) |
| GND | Ground for both sensors (via − rail) |

## Notes

- Both sensors share the 5V and GND rails, but each has its **own resistor** and its **own analog pin**, so they don't affect each other.
- FSRs have no polarity: either leg can go to 5V.
- On long breadboards, the + and − rails may be split in the middle. Keep both circuits on the same half, or bridge the gap with a jumper.
- Breadboard holes are written in lowercase (a10, e20) to distinguish them from Arduino pins (A0, A1).
