import json
import time
import tkinter as tk
import winsound

import serial

PORT = "COM14"  # Change this to your Pico's port

connection = serial.Serial(PORT, 115200, timeout=0.1)
pending_data = bytearray()
started_at = time.monotonic()

window = tk.Tk()
window.title("Pico sensor")

temperature = tk.Label(window, text="Temperature: waiting...", font=("Arial", 18))
temperature.pack(padx=20, pady=10)

humidity = tk.Label(window, text="Humidity: waiting...", font=("Arial", 18))
humidity.pack(padx=20, pady=10)

target = tk.Label(window, text="Target: waiting...", font=("Arial", 14))
target.pack(padx=20, pady=10)

warning = tk.Label(
    window, text="Waiting for temperature and target...", font=("Arial", 14, "bold")
)
warning.pack(padx=20, pady=10)
warning_active = False

serial_data = tk.Label(
    window, text=f"Connected to {PORT}; waiting for Pico data...", font=("Arial", 10)
)
serial_data.pack(padx=20, pady=10)


def update():
    global warning_active

    try:
        chunk = connection.read(connection.in_waiting or 1)
    except serial.SerialException as error:
        serial_data.config(text=f"Serial read error on {PORT}: {error}")
        return

    pending_data.extend(chunk)
    if chunk and b"\n" not in pending_data:
        serial_data.config(
            text=f"Received {len(pending_data)} bytes; waiting for the JSON line to finish"
        )
    elif not chunk and not pending_data and time.monotonic() - started_at >= 5:
        serial_data.config(text=f"No serial bytes received from {PORT} in 5 seconds")

    while b"\n" in pending_data:
        raw_line, _, remainder = pending_data.partition(b"\n")
        pending_data[:] = remainder
        line = raw_line.decode("utf-8", errors="replace").strip()
        if not line:
            continue


        try:
            data = json.loads(line)
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")

            temperature_value = data.get("temperature", data.get("temp"))
            if temperature_value is None:
                temperature.config(text="Temperature: not found in received data")
            else:
                temperature.config(text=f"Temperature: {temperature_value} °C")

            if "humidity" in data:
                humidity.config(text=f"Humidity: {data['humidity']}%")
            target_value = data.get("target_temperature")
            if target_value is not None:
                target.config(text=f"Target temperature: {target_value} °C")

            if (
                isinstance(temperature_value, (int, float))
                and not isinstance(temperature_value, bool)
                and isinstance(target_value, (int, float))
                and not isinstance(target_value, bool)
            ):
                if temperature_value >= target_value:
                    if not warning_active:
                        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    warning_active = True
                    warning.config(
                        text="WARNING: Temperature is at or above the target!",
                        fg="red",
                    )
                else:
                    warning_active = False
                    warning.config(
                        text="Temperature is below the target.",
                        fg="green",
                    )
            else:
                warning.config(
                    text="Warning unavailable: temperature or target is missing.",
                    fg="gray",
                )
        except (json.JSONDecodeError, ValueError):
            temperature.config(text="Temperature: received data is not valid JSON")

    window.after(100, update)


def close_window():
    connection.close()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", close_window)
update()
window.mainloop()