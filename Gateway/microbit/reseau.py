import radio

class RadioProtocol:
    def __init__(self, address):
        self.addr = address
        return None

    def calculateChecksum(self, message):
        print("message chksm", message)
        nleft = len(message)
        sum = 0
        pos = 0
        while nleft > 1:
            sum = ord(message[pos]) * 256 + (ord(message[pos + 1]) + sum)
            pos = pos + 2
            nleft = nleft - 2
        if nleft == 1:
            #print(len(message))
            test = ord(message[pos]) * 256
            #print(type(test))
            #print(type(sum))
            sum = sum + test
            #print(type(sum))

        sum = (sum >> 16) + (sum & 0xFFFF)
        sum += (sum >> 16)
        sum = (~sum & 0xFFFF)

        print("valeur checksm", sum)
        return sum

    def sendPacket(self, message, addrDest):
        if len(message)<251:
            encrypted_message = self.encrypt(message)
            radio.send_bytes(str(self.addr) + "|" + str(len(message)) + "|" + str(addrDest) + "|" + str(encrypted_message)+ "|" + str(self.calculateChecksum(str(encrypted_message))))

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
            print("message recu", stuff['message'])
            stuff['receivedCheckSum'] = tabRes[4]
            print("chksm recu", stuff['receivedCheckSum'])
            if self.verifyCheckSum(stuff['receivedCheckSum'], self.calculateChecksum(stuff['message'])):
                if self.addr == int(stuff['addrDest']):
                    message = self.decrypt(stuff['message'])
                    return message
            return -1
    
    def verifyCheckSum(self, checkSum, receivedCheckSum):
        print(checkSum)
        print(receivedCheckSum)
        if int(checkSum) == receivedCheckSum:
            return True
        else:
            return False

    #convert list of char to string
    def convert(self, s):
        new = ""
        for x in s:
            new += x 
        return new

    def encrypt(self, message):
        #print(len(message))
        encrypted_message = [0]*len(message) 
        for i in range (len(message)):
            ascii_char = ord(message[i]) + 4
            encrypted_message[i] = ascii_char
        #print(len(encrypted_message))
        return encrypted_message

    def decrypt(self, message):
        print(type(message))
        message = message.replace("[","")
        message = message.replace("]","")
        message = message.replace(" ","")
        print(message)
        message = message.split(",")
        print(message)
        decrypted_message = [0]*(len(message))
        for i in range (len(message)):
            encrypted_char = chr(message[i]-4)
            decrypted_message[i] = encrypted_char
        return self.convert(decrypted_message)

    