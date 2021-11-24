import radio

class RadioProtocol:
    def __init__(self, address):
        self.addr = address
        return None

    def calculateChecksum(self, message):
        nleft = len(message)
        sum = 0
        pos = 0
        while nleft > 1:
            sum = ord(message[pos]) * 256 + (ord(message[pos + 1]) + sum)
            pos = pos + 2
            nleft = nleft - 2
        if nleft == 1:
            test = ord(message[pos]) * 256
            sum = sum + test

        sum = (sum >> 16) + (sum & 0xFFFF)
        sum += (sum >> 16)
        sum = (~sum & 0xFFFF)

        return sum

    def sendPacket(self, message, addrDest):
        if len(message)<251:
            encrypted_message = self.encrypt(message)
            radio.send_bytes("" + str(self.addr) + "|" + str(len(message)) + "|" + str(addrDest) + "|" + str(encrypted_message)+ "|" + str(self.calculateChecksum(str(encrypted_message))))

    def receivePacket(self, packet):
        if packet is None:
            return 0
        else:
            print(packet)
            tabRes = packet.format(1).split("|")
            if len(tabRes) > 5:
                return -1
            stuff = dict()
            stuff['addrInc'] = tabRes[0]
            stuff['lenMess'] = tabRes[1]
            stuff['addrDest'] = tabRes[2]
            stuff['message'] = tabRes[3]
            stuff['receivedCheckSum'] = tabRes[4]
            if self.verifyCheckSum(stuff['receivedCheckSum'], self.calculateChecksum(stuff['message'])):
                if self.addr == int(stuff['addrDest']):
                    message = self.decrypt(stuff['message'])
                    return message
            return -1
    
    def verifyCheckSum(self, checkSum, receivedCheckSum):
        if int(checkSum) == receivedCheckSum:
            return True
        else:
            return False

    def convert(self, s):
        new = ""
        for x in s:
            new += x 
        return new

    def encrypt(self, message):
        encrypted_message = [0]*len(message) 
        for i in range (len(message)):
            ascii_char = ord(message[i]) + 4
            encrypted_message[i] = ascii_char
        return encrypted_message

    def decrypt(self, message):
        message = message.replace("[","")
        message = message.replace("]","")
        message = message.replace(" ","")
        message = message.split(",")
        message = list(map(int,message))
        decrypted_message = [0]*(len(message))
        for i in range (len(message)):
            encrypted_char = chr(message[i]-4)
            decrypted_message[i] = encrypted_char
        return self.convert(decrypted_message)

    