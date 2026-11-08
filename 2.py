import machine
import utime
import dht

pin = machine.Pin(0, machine.Pin.OUT, machine.Pin.PULL_DOWN)
sensor = dht.DHT11(pin)

while True:
    print("temperature：{} ℃  humidity：{} %".format(sensor.temperature, sensor.humidity))
    utime.sleep(1)   