
import zlib
import sys

def check(file):
    with open(file, "rb") as f:
        bytes = f.read()
    checksum = zlib.crc32(bytes)
    print(checksum)

def main():
    check(sys.argv[1])

if __name__ == '__main__':
    main()


