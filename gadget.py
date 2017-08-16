import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import dht
import time



temp_form='Temp: {:9.1f}F'
max_form='Max Temp: {:5.1f}F'
max_place_holder='Max Temp:   None'
min_form='Min Temp: {:5.1f}F'
min_place_holder='Min Temp:   None'
max_temp=None
min_temp=None
humdity_form='Humidity: {:5.0f}%'

d1=None
d2=None
d5=None
i2c=None
oled=None
sensor=None
ip_address=None
run_ap=False

def CtoF(c):
    return (1.8 * c) + 32

def init(do_ap=False):
    global d1,d2,d5,i2c,oled,sensor,ip_address,run_ap
    d1=Pin(5) # SCL
    d2=Pin(4) # SDA
    d5=Pin(14, Pin.IN) # DHT Sense
    i2c=I2C(scl=d1, sda=d2)
    oled=SSD1306_I2C(128, 64, i2c)
    sensor=dht.DHT22(d5)

    oled.fill(0)
    oled.text("Loading...", 0, 30)
    oled.show()

    run_ap=do_ap
    if do_ap:
        import network
        import ubinascii
        ap_if=network.WLAN(network.AP_IF)
        essid=b"EnvPy-%s" % ubinascii.hexlify(ap_if.config("mac")[-3:])
        ap_if.active(True)
        ap_if.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=b"<HAHAHAHAHA>")

        ip_address=b"AP: "+ ap_if.ifconfig()[0]

        print("AP Configured")

def report_temp(display, sense):
    global max_temp, min_temp, ip_address,run_ap
    sense.measure()
    c=sense.temperature()
    hum=sense.humidity()
    f=CtoF(c)
    display.fill(0)
    display.text(temp_form.format(f), 0, 0)
    if max_temp is None:
        display.text(max_place_holder, 0, 10)
        max_temp=f
    else:
        display.text(max_form.format(max_temp), 0, 10)
        max_temp=max(f, max_temp)
        
    if min_temp is None:
        display.text(min_place_holder, 0, 20)
        min_temp=f
    else:
        display.text(min_form.format(min_temp), 0, 20)
        min_temp=min(f, min_temp)
        
    display.text(humdity_form.format(hum), 0, 30)
    
    if run_ap:
        display.text(ip_address, 0 , 50)
    
    display.show()
    
def run():
    while True:
        report_temp(oled, sensor)
        time.sleep(15)