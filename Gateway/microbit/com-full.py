from microbit import *
import radio
import reseau

radio.config(length=251, group=64)
radio.on()
reseau = reseau.RadioProtocol(2)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

Packet_end = "[END]"

while True:
    message = reseau.receivePacket(radio.receive_bytes())
    if message:
        uart.write(message + Packet_end)
    if uart.any():
        content = uart.read()
        packet = content[:2]
        if(packet == 'TL'):
            reseau.sendPacket("TL", 1)
        elif(packet == 'LT'):
            reseau.sendPacket("LT", 1)
    sleep(1000)
