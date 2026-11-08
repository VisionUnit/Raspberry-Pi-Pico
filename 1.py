from machine import Pin
import time

# Set up LED on GPIO 25
led = Pin(0, Pin.OUT)

# Set up Button on GPIO 30
button = Pin(1, Pin.IN, Pin.PULL_UP)

# Variable to track LED state
led_state = False

while True:
    # Check if button is pressed (active low)
    if button.value() == 0:
        # Toggle LED state
        led_state = not led_state
        led.value(led_state)
        
        # Debounce delay
        time.sleep(0.2)
        
        # Wait for button release
        while button.value() == 0:
            time.sleep(0.1)
        
        # Additional debounce delay
        time.sleep(0.2)
    
    time.sleep(0.01)