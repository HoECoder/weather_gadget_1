# Weather Gadget 1
Weather Gadget in MicroPython on ESP8266 w/OLED and DHT22

This little gadget is written in MicroPython for the ESP8266. It has a 128x64 pixel SSD1306 OLED display that operates over I2C.

The DHT22 sensor is mounted on a small PCB with the proper pullup already soldered in.

It loops once every 15 seconds, showing the current temp, the max and min since last boot, and the current humidity.

It is currently configured to show in Fahrenheit.

It uses 4 of the six potential lines one can use to draw with on the OLED module.
