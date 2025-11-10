import os
import time

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# paths
DATA_PATH = "data"
PLAINTEXT_PATH = "data/plaintexts"
KEYS_PATH = "data/keys.txt"

# des block size
BLOCK_SIZE = 8

# load files 
def load_plaintexts():
    number_txt_file = os.path.join(PLAINTEXT_PATH, "numbers.txt")
    letter_txt_file = os.path.join(PLAINTEXT_PATH, "letters.txt")

    with open(number_txt_file, "r") as f:
        numbers = f.read().splitlines()
    
    with open(letter_txt_file, "r") as f:
        letters = f.read().splitlines()
    
    return numbers, letters

def load_keys():
    with open(KEYS_PATH, "r") as f:
        keys = f.read().splitlines()

    return keys

# des encryption
def des_encrypt(key, plaintext):
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    pad_txt = pad(plaintext.encode('utf-8'), BLOCK_SIZE)

    return cipher.encrypt(pad_txt)

# des decryptions
def des_decrypt(key, ciphertext):
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)

    return unpad(decrypted, BLOCK_SIZE).decode('utf-8')

# test plaintext key sensitivity
def plaintext_key_sensitivity():
    numbers, letters = load_plaintexts()
    keys = load_keys()

    for pt in letters + numbers:
        cipher1 = des_encrypt(keys[0], pt)
        cipher2 = des_encrypt(keys[1], pt)

        print(f"\nPlaintext: {pt}")
        print(f"Key 1: {keys[0]} -> Ciphertext: {cipher1.hex().upper()}")
        print(f"Key 2: {keys[1]} -> Ciphertext: {cipher2.hex().upper()}")

if __name__ == "__main__":
    plaintext_key_sensitivity()