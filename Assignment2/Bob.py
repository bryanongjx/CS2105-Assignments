import sys
from socket import *
import zlib

def split_packet(packet):
    checksum = int.from_bytes(packet[:4], 'big')
    seq_ack = int.from_bytes(packet[4:5], 'big')
    data = packet[5:].decode()
    return checksum, seq_ack, data

def create_ack(seq_num):
    packet = seq_num.to_bytes(1, 'big')
    checksum = zlib.crc32(packet).to_bytes(4, 'big')
    packet = checksum + packet
    return packet

def check_packet(packet):
    expected_checksum = int.from_bytes(packet[:4], 'big')
    actual_checksum = zlib.crc32(packet[4:])
    return expected_checksum == actual_checksum

def Bob():

    serverPort = int(sys.argv[1])
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    expected_seq_num = 0

    while True:
        # receive packet
        received_packet, clientAddress = serverSocket.recvfrom(64)
        
        # check if packet corrupted
        if check_packet(received_packet):
            checksum, seq_num, data = split_packet(received_packet)
            
            #check if seq num matches expected seq num
            if seq_num == expected_seq_num:
                print(data, end = "")
                expected_seq_num = 1 - seq_num
               
        # send out ack_packet
        ack_packet = create_ack(seq_num)
        serverSocket.sendto(ack_packet, clientAddress)

    serverSocket.close()

if __name__ == "__main__":
    Bob()
