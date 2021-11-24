from microbit import *
import radio
import reseau
import uart

radio.config(length=251, group=64)
radio.on()
reseau = reseau.RadioProtocol(2)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

while True:
    message = reseau.receivePacket(radio.receive_bytes())
    if message:
        uart.write(message)
    if uart.any():
        content = uart.read()
        if(content == 'TL'):
            reseau.sendPacket("TL", 1)
        else if(content == 'LT'):
            reseau.sendPacket("LT", 1)
    sleep(1000)
