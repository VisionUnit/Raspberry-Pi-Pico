from machine import Pin
from time import sleep
import dht

# Initialize sensor on a GPIO pin (e.g., Pin 22)
# Use dht.DHT11(Pin(22)) for DHT11 sensors
sensor = dht.DHT22(Pin(0))

while True:
    try:
        sleep(2)  # DHT sensors require a delay between readings
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f"Temperature: {temp:.1f}°C, Humidity: {hum:.1f}%")
    except OSError as e:
        print("Failed to read sensor.")