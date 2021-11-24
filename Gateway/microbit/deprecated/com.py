import radio
from microbit import *
import reseau

radio.config(group=64)
radio.on()
reseau = reseau.RadioProtocol(1)

while True:
    message = reseau.receivePacket(radio.receive_bytes())
    if message:
        display.scroll(message)
    if button_a.is_pressed():
        reseau.sendPacket("Salut", 2)
    sleep(1000)
