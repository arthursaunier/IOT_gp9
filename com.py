from microbit import *
import radio
import reseau



radio.config(group=2)
radio.on()
reseau = reseau.RadioProtocol(2)

while True:
    message = reseau.receivePacket(radio.receive_bytes())
    if message:
        display.scroll(message)
    if button_a.is_pressed():
        reseau.sendPacket("Salut", 1)
    sleep(1000)