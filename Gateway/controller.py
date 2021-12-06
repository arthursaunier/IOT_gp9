# Program to control passerelle between Android application
# and micro-controller through USB tty
import time
import argparse
import signal
import sys
import socket
import socketserver
import serial
import threading

HOST           = "192.168.1.90"
UDP_PORT       = 10000
MICRO_COMMANDS = ["TL" , "LT"]
FILENAME        = "log"
PACKET_END = "[END]"

#log and filing
from data.log import Log
from data.file import File
file = File(FILENAME)
from data.format import Format


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("request received")
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        data = data.decode()
        if data != "":
                if data in MICRO_COMMANDS: # Send message through UART
                        #ajoute la fin de packet pour identifier les données
                        sendUARTMessage(data + PACKET_END)
                                
                elif data == "update": # Sent last value received from micro-controller
                        print("update received")
                        #récupère le dernier log venant des microbits
                        last_log = file.get_last_log()
                        if last_log != None:
                                #formate le log avant envoie a l'appli
                                data = Format.reform(last_log)
                                print("sending data to app")
                                socket.sendto(data, self.client_address) 
                                     
                else:
                        print("Unknown message: ",data)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


# send serial message 
SERIALPORT = "/COM5"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():        
        # ser = serial.Serial(SERIALPORT, BAUDRATE)
        ser.port=SERIALPORT
        ser.baudrate=BAUDRATE
        ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        ser.parity = serial.PARITY_NONE #set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        ser.timeout = None          #block read

        # ser.timeout = 0             #non-block read
        # ser.timeout = 2              #timeout block read
        ser.xonxoff = False     #disable software flow control
        ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        #ser.writeTimeout = 0     #timeout for write
        print ('Starting Up Serial Monitor')
        try:
                ser.open()
        except serial.SerialException:
                print("Serial {} port not available".format(SERIALPORT))
                exit()



def sendUARTMessage(msg):
    ser.write(msg.encode())
    print("Message <" + msg + "> sent to micro-controller." )


# Main program logic follows:
if __name__ == '__main__':
        initUART()
        #f= open(FILENAME,"a")
        print ('Press Ctrl-C to quit.')

        server = ThreadedUDPServer((HOST, UDP_PORT), ThreadedUDPRequestHandler)

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True

        try:
                server_thread.start()
                print("Server started at {} port {}".format(HOST, UDP_PORT))
                while ser.isOpen() : 
                        # time.sleep(100)
                        if ser.in_waiting > 0:
                                # Read data out of the buffer until a carriage return / new line is found
                                data_str = ser.readline()
                                ser.flush()

                                #decode le byte et récupère les données nécéssaires
                                data_str = data_str.decode()
                                #verifie présence d'une trame (avec le packet_end présent)
                                if(data_str.find(PACKET_END) != -1):
                                        #recup trame en enlevant la fin de la trame
                                        data = str(data_str)[:data_str.find("[END]")]
                                        #formatage des infos pour sauvegarde dans le fichier/log
                                        parsed = Format.parse(data)
                                        log = Log.from_dict(parsed)

                                        #sauvegarde le log ds un fichier
                                        file.save(log)
                                
        except (KeyboardInterrupt, SystemExit):
                server.shutdown()
                server.server_close()
                ser.close()
                exit()