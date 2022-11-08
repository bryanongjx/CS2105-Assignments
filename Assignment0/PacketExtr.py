import sys

def read_bytes(n):
    return sys.stdin.buffer.read1(n)

def packet_extr():
    sys.stdout.buffer.flush()

    while read_bytes(6):
        curr = read_bytes(1)
        size_array = bytearray()

        while curr != b'B':
            size_array.extend(curr)
            curr = read_bytes(1)

        size = int(size_array.decode())
        payload = read_bytes(size)
        sys.stdout.buffer.write(payload)
        sys.stdout.buffer.flush()

if __name__ == '__main__':
    packet_extr()