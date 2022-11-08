import os.path
import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5, AES
from Cryptodome.Random import get_random_bytes
from socket import *

rsa_key_len = int(2048/8)


def load_rsa_key(f_name_key="test/rsa_key.bin"):
    """
    load the public RSA key
    :return: RSA key
    """
    key = RSA.importKey(open(f_name_key).read())
    return key


# connect to the server
if len(sys.argv) < 5:
    print ("Usage: python3 ", os.path.basename(__file__), "key_file_name data_file_name hostname/IP port")

else:
    key_file_name   = sys.argv[1]
    data_file_name  = sys.argv[2]
    serverName      = sys.argv[3]
    serverPort      = int(sys.argv[4])
    print (serverName, serverPort)

    rsa_key     = load_rsa_key()

    # connect to the server
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    # get the session key
    # first 256 bytes sent by the server is the RSA encrypted session key
    cipher_rsa = PKCS1_v1_5.new(rsa_key)

    cipher_text = clientSocket.recv(256)
    sentinel = get_random_bytes(16)
    session_key = cipher_rsa.decrypt(cipher_text, sentinel)

    # write the session key to the file "key_file_name"
    with open(key_file_name, "wb") as f:
        f.write(session_key)

    # get the data and write to file "data_file_name"
    cipher_aes = AES.new(session_key, AES.MODE_ECB)

    # get the data from server
    data = clientSocket.recv(16)
    output = b''
    while data:
        decrypted_data = cipher_aes.decrypt(data)
        output += decrypted_data
        data = clientSocket.recv(16)

    with open(data_file_name, "wb") as g:
        g.write(output)


