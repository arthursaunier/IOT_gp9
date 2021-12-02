from microbit import *
import radio
import reseau

from ssd1306 import initialize
from ssd1306 import clear_oled
from ssd1306_text import *

initialize(pinReset = pin0)
clear_oled()
radio.config(length=251, group=64)
radio.on()
reseau = reseau.RadioProtocol(1)

Temp = 0
Lum = 0
oldTemp = 0
oldLum = 0

while True:
    Temp = temperature()
    Lum = display.read_light_level()
    message = reseau.receivePacket(radio.receive_bytes())
    if message:
        #display.scroll(message)
        if message == 'TL':
            add_text(5,0,"T:" + str(Temp))
            add_text(5,3,"L:" + str(Lum))
        elif message == 'LT':
            add_text(5,0,"L:" + str(Lum))
            add_text(5,3,"T:" + str(Temp))
    else:
        add_text(2,2,"T:" + str(temperature()) + " L:"+ str(display.read_light_level()))
    if (Temp != oldTemp or Lum != oldLum):
        reseau.sendPacket(str(Temp) + ":"+ str(Lum), 2)
        oldLum = Lum
        oldTemp = Temp
    sleep(2000)
