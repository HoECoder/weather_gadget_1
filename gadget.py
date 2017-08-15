import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import dht
import time

import network
import ubinascii

ap_if = network.WLAN(network.AP_IF)
essid = b"EnvPy-%s" % ubinascii.hexlify(ap_if.config("mac")[-3:])
ap_if.active(True)
ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password = b"<HAHAHAHAHA>")

ip_address = b"AP: "+ ap_if.ifconfig()[0]

temp_form = 'Temp: {:9.1f}F'
max_form = 'Max Temp: {:5.1f}F'
max_place_holder = 'Max Temp:   None'
min_form = 'Min Temp: {:5.1f}F'
min_place_holder = 'Min Temp:   None'
max_temp = None
min_temp = None
humdity_form = 'Humidity: {:5.0f}%'

def CtoF(c):
    return (1.8 * c) + 32

def report_temp(display, sense):
    global max_temp, min_temp, ip_address
    sense.measure()
    c = sense.temperature()
    hum = sense.humidity()
    f = CtoF(c)
    oled.fill(0)
    oled.text(temp_form.format(f), 0, 0)
    if max_temp is None:
        oled.text(max_place_holder, 0, 10)
        max_temp = f
    else:
        oled.text(max_form.format(max_temp), 0, 10)
        max_temp = max(f, max_temp)
        
    if min_temp is None:
        oled.text(min_place_holder, 0, 20)
        min_temp = f
    else:
        oled.text(min_form.format(min_temp), 0, 20)
        min_temp = min(f, min_temp)
        
    oled.text(humdity_form.format(hum), 0, 30)
    
    oled.text(ip_address, 0 , 50)
    
    oled.show()

d1 = Pin(5) # SCL
d2 = Pin(4) # SDA
d5 = Pin(14, Pin.IN) # DHT Sense
i2c = I2C(scl = d1, sda = d2)
oled = SSD1306_I2C(128, 64, i2c)
sensor = dht.DHT22(d5)

def run():
    while True:
        report_temp(oled, sensor)
        time.sleep(15)