import sys
from socket import *
import zlib

def Alice():

    def read_stdin():
        num_bytes = 59
        data = bytearray()
        while num_bytes > 0:
            message = sys.stdin.buffer.read1(num_bytes)
            if len(message) == 0:
                break
            data.extend(message)
            num_bytes -= len(message)
        return data
    
    # format of packet is checksum(4bytes), seq num(1byte), data(59 bytes)
    def create_packet(seq_num, data):
        packet = seq_num.to_bytes(1, 'big')
        packet = packet + data
        checksum = zlib.crc32(packet).to_bytes(4, 'big')
        packet = checksum + packet
        return packet

    def check_packet(packet):
        expected_checksum = int.from_bytes(packet[:4], 'big')
        actual_checksum = zlib.crc32(packet[4:])
        return expected_checksum == actual_checksum

    def split_ack_packet(packet):
        checksum = int.from_bytes(packet[:4], 'big')
        seq_ack = int.from_bytes(packet[4:5], 'big')
        return checksum, seq_ack

    serverName = 'localhost'
    serverPort = int(sys.argv[1])
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(0.05)
    seq_num = 0
    data = read_stdin()
        
    while True:
        try:
            if len(data) == 0:
                break
            #send packet
            packet_to_send = create_packet(seq_num, data)
            clientSocket.sendto(packet_to_send, (serverName, serverPort))
            
            #receive ack packet
            ack_packet, serverAddress = clientSocket.recvfrom(64)

            # check if packet corrupted
            if check_packet(ack_packet):
                checksum, ack_seq_num = split_ack_packet(ack_packet)
                # check if ack seq num matches seq num, if so, can send next packet and update seq num
                if ack_seq_num == seq_num:
                    data = read_stdin()
                    seq_num = 1 - seq_num
        except timeout:
            pass

    clientSocket.close()

if __name__ == "__main__":
    Alice()
