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
affichage = 0

while True:
    Temp = temperature()
    Lum = display.read_light_level()
    message = reseau.receivePacket(radio.receive_bytes())
    if (message != 0):
        if message == 'TL':
            affichage = 1
        elif message == 'LT':
            affichage = 0
    if (affichage == 0):
        add_text(0, 1, "Temp : " + str(Temp) + " C")
        add_text(0, 2, "Lum : " + str(Lum) + " lm ")
    else:
        add_text(0, 1, "Lum : " + str(Lum) + " lm ")
        add_text(0, 2, "Temp : " + str(Temp) + " C")
    if (Temp != oldTemp or Lum != oldLum):
        reseau.sendPacket(str(Temp) + ":"+ str(Lum), 2)
        oldLum = Lum
        oldTemp = Temp
    sleep(2000)
