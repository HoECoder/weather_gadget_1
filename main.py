import gadget

from machine import Pin, I2C
import dht
import time

d1=Pin(5) # SCL
d2=Pin(4) # SDA
d5=Pin(14, Pin.IN) # DHT Sense
i2c=I2C(scl=d1, sda=d2)
sensor = dht.DHT11(d5)

g = gadget.Gadget(i2c,sensor)
g.init()

while True:
    g.measure()
    g.report()
    time.sleep(15)
    
