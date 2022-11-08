# !/usr/bin/env python3
import os
import sys
from Cryptodome.Hash import SHA256

if len(sys.argv) < 3:
    print("Usage: python3 ", os.path.basename(__file__), "key_file_name document_file_name")
    sys.exit()

key_file_name   = sys.argv[1]
file_name       = sys.argv[2]

# get the authentication key from the file
with open(key_file_name, "rb") as f:
    authentication_key = f.read()

# read the input file

# First 32 bytes is the message authentication code
with open(file_name, "rb") as f:
    mac_from_file = f.read(32)

# Use the remaining file content to generate the message authentication code
with open(file_name, "rb") as f:
    data = f.read()[32:]

    # combine message + s
    m_s = data + authentication_key

    # hash
    hashed_obj = SHA256.new(data = m_s)

    # digest to convert hashed_obj back to bytes
    mac_generated = hashed_obj.digest()

if mac_from_file == mac_generated:
    print('yes')
else:
    print ('no')
