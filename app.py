from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
from base64 import b64encode, b64decode
import sys


def encrypt(file_name):
    key = Random.new().read(AES.block_size)
    write_key(key)
    with open(file_name, 'rb') as f:
        data = f.read()
        cipher = AES.new(key, AES.MODE_CFB)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher.iv).decode('UTF-8')
        ciphertext = b64encode(ciphertext).decode('UTF-8')
    f.close()
    with open(file_name + '.enc', 'w') as raw_data:
        raw_data.write(iv + ciphertext)
    raw_data.close()


def decrypt(file_name):
    key = read_key()
    with open(file_name, 'rb') as f:
        data = f.read()
        length = len(data)
        iv = data[:24]
        iv = b64decode(iv)
        ciphertext = data[24:length]
        ciphertext = b64decode(ciphertext)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        decrypted = cipher.decrypt(ciphertext)
        decrypted = unpad(decrypted, AES.block_size)
        with open('decrypted_' + file_name[:-4], 'wb') as decrypted_f:
            decrypted_f.write(decrypted)
        decrypted_f.close()


def write_key(key):
    with open('key.txt', 'wb') as f:
        f.write(key)


def read_key():
    with open('key.txt', 'rb') as f:
        data = f.read()
        return data


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--encrypt", help="moznost na AES sifrovanie")
parser.add_argument("--decrypt", help="moznost na AES desifrovanie")
args = parser.parse_args()

if (sys.argv[2] is None):
    print("Missing an input file.")
file_name = sys.argv[2]
if args.encrypt:
    encrypt(file_name)
elif args.decrypt:
    decrypt(file_name)
else:
    print("Missing an input file.")
