import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import dht
import time
from micropython import const

temp_form='Temp: {:9.1f}F'
max_form='Max Temp: {:5.1f}F'
min_form='Min Temp: {:5.1f}F'
humdity_form='Humidity: {:5.0f}%'

smooth_factor=const(4)

def CtoF(c):
    return (1.8 * c) + 32
    
def smoothing_func(previous,current):
    return (current+smooth_factor*previous)/(smooth_factor+1)

class Gadget:
    def __init__(self,i2c, sensor, width=128, height=64):
        self.previous_c = None
        self.current_c = None
        self.width = width
        self.height = height
        self.i2c = i2c
        self.sensor = sensor
        self.oled = None
        self.max_temp = None
        self.min_temp = None
        
    def init(self):
        self.oled = oled=SSD1306_I2C(self.width, self.height, self.i2c)
        self.oled.fill(0)
        self.oled.text("Loading...", 0, 30)
        self.oled.show()
        
    def measure(self):
        self.sensor.measure()
        
    def report(self):
        c=self.sensor.temperature()
        p = self.previous_c
        if p is None:
            p=c
        c=smoothing_func(p,c)
        p=c
        self.current_c=c
        self.previous_c=p
        hum=self.sensor.humidity()
        f=CtoF(c)
        self.oled.fill(0)
        self.oled.text(temp_form.format(f), 0, 0)
        if self.max_temp is None:
            self.oled.text(max_form.format(f), 0, 10)
            self.max_temp=f
        else:
            self.oled.text(max_form.format(self.max_temp), 0, 10)
            self.max_temp=max(f, self.max_temp)
            
        if min_temp is None:
            self.oled.text(min_form.format(f), 0, 20)
            self.min_temp=f
        else:
            self.oled.text(min_form.format(self.min_temp), 0, 20)
            self.min_temp=min(f, self.min_temp)
            
        self.oled.text(humdity_form.format(hum), 0, 30)
        
        self.oled.show()

