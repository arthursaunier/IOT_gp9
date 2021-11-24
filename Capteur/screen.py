from microbit import *
import radio
import reseau

from ssd1306 import initialize
from ssd1306 import clear_oled
from ssd1306_text import *

initialize(pinReset = pin0)
clear_oled()
radio.config(group=3)
radio.on()
reseau = reseau.RadioProtocol(1)

while True:
    message = reseau.receivePacket(radio.receive_bytes())
    if message:
        display.scroll(message)
    if message == 'TL':
        add_text(5,0,"T:" + str(temperature()))
        add_text(5,3,"L:" + str(display.read_light_level()))
    if message == 'LT':
        add_text(5,0,"L:" + str(display.read_light_level()))
        add_text(5,3,"T:" + str(temperature()))
    if button_a.is_pressed():
        reseau.sendPacket(str(temperature()) + ":"+ str(display.read_light_level()), 2)
    sleep(1000)
