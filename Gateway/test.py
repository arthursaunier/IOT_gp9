    

def encrypt(message):
    #print(len(message))
    encrypted_message = [0]*len(message) 
    for i in range (len(message)):
        ascii_char = ord(message[i]) + 4
        encrypted_message[i] = ascii_char
    #print(len(encrypted_message))
    return encrypted_message

def decrypt(message):
    #print(len(message))
    decrypted_message = [0]*(len(message))
    for i in range (len(message)):
        encrypted_char = chr(message[i]-4)
        decrypted_message[i] = encrypted_char
    return convert(decrypted_message)

#convert list of char to string
def convert(s):
    new = ""
    for x in s:
        new += x 
    return new

if __name__ == "__main__":
    message = "hello"
    encrypt_mess = (encrypt(message))
    print(encrypt_mess)

    decrypt_mess = decrypt(encrypt_mess)
    print(decrypt_mess)
    