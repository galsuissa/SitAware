import serial

PORT = "COM3"        # the port shown in the Arduino IDE
BAUD_RATE = 9600     # must match Serial.begin(9600) in the firmware


def main():
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as arduino:
        print(f"Connected to {PORT}. Press Ctrl+C to stop.")
        while True:
            raw = arduino.readline()                       # read one line (bytes)
            line = raw.decode("utf-8", errors="ignore").strip()
            if line:                                       # skip empty lines
                print(line)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
