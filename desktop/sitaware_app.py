import tkinter as tk

import serial

from read_serial import PORT, BAUD_RATE, parse_line

UPDATE_INTERVAL_MS = 100   # how often the window checks for new data

# Text and background colour for each state (same numbers as the firmware enum)
STATE_DISPLAY = {
    0: ("No one sitting", "#9e9e9e"),             # grey
    1: ("Sitting - no back support", "#f39c12"),  # orange
    2: ("Sitting - leaning back", "#27ae60"),     # green
}
ALERT_TEXT = "Please sit right and lean back!"
ALERT_COLOR = "#e74c3c"                           # red


class SitAwareApp:
    def __init__(self, root, arduino):
        self.root = root
        self.arduino = arduino

        root.title("SitAware")
        root.geometry("460x240")

        self.state_label = tk.Label(root, text="Waiting for data...",
                                    font=("Segoe UI", 20, "bold"), fg="white")
        self.state_label.pack(expand=True)

        self.alert_label = tk.Label(root, text="", font=("Segoe UI", 14, "bold"), fg="white")
        self.alert_label.pack()

        self.values_label = tk.Label(root, text="", font=("Segoe UI", 10), fg="white")
        self.values_label.pack(pady=10)

        self.set_background(STATE_DISPLAY[0][1])
        self.check_serial()   # start the repeating check

    def set_background(self, color):
        """Paint the window and all labels in one colour."""
        self.root.configure(bg=color)
        for label in (self.state_label, self.alert_label, self.values_label):
            label.configure(bg=color)

    def check_serial(self):
        """Read every line that has already arrived, then schedule the next check."""
        while self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode("utf-8", errors="ignore").strip()
            data = parse_line(line)
            if data is not None:              # ignore non-data lines (e.g. alert messages)
                self.update_display(data)

        self.root.after(UPDATE_INTERVAL_MS, self.check_serial)

    def update_display(self, data):
        """Show the state, values and alert from one parsed data line."""
        text, color = STATE_DISPLAY.get(data["state"], ("Unknown state", "#555555"))

        if data["alert"]:
            color = ALERT_COLOR
            self.alert_label.configure(text=ALERT_TEXT)
        else:
            self.alert_label.configure(text="")

        self.state_label.configure(text=text)
        self.values_label.configure(text=f"Seat: {data['seat']}    Back: {data['back']}")
        self.set_background(color)


def main():
    try:
        arduino = serial.Serial(PORT, BAUD_RATE, timeout=0.1)
    except serial.SerialException as error:
        print(f"Could not open {PORT}: {error}")
        print("Is the Arduino plugged in, and are the Serial Monitor and read_serial.py closed?")
        return

    with arduino:              # the port is closed automatically when the window closes
        root = tk.Tk()
        SitAwareApp(root, arduino)
        root.mainloop()


if __name__ == "__main__":
    main()
