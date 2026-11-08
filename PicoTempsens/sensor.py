from machine import Pin
from time import sleep, time
import dht
from rotary_irq_rp2 import RotaryIRQ
import json

status = {
    "temperature": 0.0,
    "humidity": 0.0,
    "target_temperature": 25,
    "target_humidity": 60,
    "overtarget_temperature": False,
    "encoder_mode": "temperature"
}

def send_status():
    print(json.dumps(status))


def getmaxtemp(iInnitmaxtemp, icurrent_val, inew_val):
    imaxtemp = 0
    iicurrent_val = icurrent_val  # Track the last known value of the encoder
    while True:
        
        while True:  # The encoder value has changed
            imaxtemp = iInnitmaxtemp + inew_val            
            inew_val = rotary.value()  # What is the encoder value right now
            #print('Encoder value:', inew_val)  # Do something with the new value
            #print("Max temperature set to:", imaxtemp)
            status["target_temperature"] = imaxtemp
            send_status()
            if icurrent_val != inew_val:
                icurrent_val = inew_val
            else:
                break
            sleep(0.1)  # Small delay to avoid rapid changes
        if iicurrent_val == inew_val:
            return (imaxtemp, icurrent_val)
        iicurrent_val = inew_val
        sleep(1)



rotary = RotaryIRQ(14, 15)
Maxtemp = 25
Innitmaxtemp = Maxtemp
current_val = 0  # Track the last known value of the encoder
# Initialize sensor on a GPIO pin (e.g., Pin 22)
# Use dht.DHT11(Pin(22)) for DHT11 sensors
btn = Pin(12, Pin.IN, Pin.PULL_UP)
sensor = dht.DHT11(Pin(28))
LED_PIN1 = 0  # GPIO pin for the LED
led1 = Pin(LED_PIN1, Pin.OUT)
LED_PIN2 = 2  # GPIO pin for the second LED
led2 = Pin(LED_PIN2, Pin.OUT)
LED_PIN3 = 4  # GPIO pin for the third LED
led3 = Pin(LED_PIN3, Pin.OUT)
while True:
    try:
        if btn.value() == 0:  # Has the button been pressed?
            #print("Reset encoder to:", 0)
            rotary.reset() # Resets the rotary library's internal counter back to zero
                
            sleep(0.25) # A small delay to wait for the button to stop being pressed
            #print('x')        
        
        new_val = rotary.value()  # What is the encoder value right now?
    
        if current_val != new_val:  # The encoder value has changed!
            Maxtemp, current_val = getmaxtemp(Innitmaxtemp, current_val, new_val)

        sleep(2)  # DHT sensors require a delay between readings
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        status["temperature"] = temp
        status["humidity"] = hum
        #print(f"Temperature: {temp: .1f}°C, Humidity: {hum:.1f}%")
        if temp >= Maxtemp:  # Example threshold for high temperature
            #print("Warning: High temperature detected!")
            status["overtarget_temperature"] = True
            led1.value(1)  # Turn on LED
            led2.value(0)  # Turn off LED
        else:
            led1.value(0)  # Turn off LED
            status["overtarget_temperature"] = False
            led2.value(1)  # Turn on LED
        send_status()
    except OSError as e:
        print("Failed to read sensor.")