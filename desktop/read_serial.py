import serial

PORT = "COM3"        # the port shown in the Arduino IDE
BAUD_RATE = 9600     # must match Serial.begin(9600) in the firmware

# The fields every data line must contain (must match the firmware output)
REQUIRED_KEYS = {"seat", "back", "state", "alert"}

# Same order as the SittingState enum in the firmware
STATE_NAMES = {0: "NOT_SITTING", 1: "SITTING_NOT_LEANING", 2: "SITTING_LEANING"}


def parse_line(line):
    """Parse 'seat:1016,back:0,state:1,alert:0' into a dict, or return None if the line isn't valid data."""
    data = {}
    parts = line.split(",")

    try:
        for part in parts:
            key, value = part.split(":")
            value = int(value)
            data[key] = value

    except ValueError:
        return None

    if data.keys() != REQUIRED_KEYS:
        return None

    return data


def format_data(data):
    """Turn a parsed data dict into a readable line."""
    state_name = STATE_NAMES.get(data["state"], "UNKNOWN")
    alert_text = "YES" if data["alert"] else "no"
    return f"Seat: {data['seat']:4} | Back: {data['back']:4} | State: {state_name:19} | Alert: {alert_text}"


def main():
    with serial.Serial(PORT, BAUD_RATE, timeout=1) as arduino:
        print(f"Connected to {PORT}. Press Ctrl+C to stop.")
        while True:
            raw = arduino.readline()                       # read one line (bytes)
            line = raw.decode("utf-8", errors="ignore").strip()
            if not line:                                   # skip empty lines
                continue

            data = parse_line(line)
            if data is None:
                print(line)                                # not data, e.g. an alert message
            else:
                print(format_data(data))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
