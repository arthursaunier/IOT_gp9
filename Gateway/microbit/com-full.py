from microbit import *
import radio
import reseau

radio.config(length=251, group=64)
radio.on()
reseau = reseau.RadioProtocol(2)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

PACKET_END = "[END]"

while True:
    message = reseau.receivePacket(radio.receive_bytes())
    if message:
        uart.write(message + PACKET_END)
    if uart.any():
        content = uart.read()
        packet = str(content[:2])
        if(packet == "b'TL'"):
            reseau.sendPacket("TL", 1)
        elif(packet == "b'LT'"):
            reseau.sendPacket("LT", 1)
    sleep(1000)
