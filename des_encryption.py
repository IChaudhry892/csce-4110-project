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

def bit_difference(cipher1, cipher2):
    diff = 0
    for b1, b2 in zip(cipher1, cipher2):
        xor = b1 ^ b2  # xor shows which bits differ
        diff += bin(xor).count("1")
    return diff

# des encryption
def des_encrypt(key, plaintext):
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    pad_txt = pad(plaintext.encode('utf-8'), BLOCK_SIZE)

    return cipher.encrypt(pad_txt)

# des decryption
def des_decrypt(key, ciphertext):
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)

    return unpad(decrypted, BLOCK_SIZE).decode('utf-8')

# test plaintext key sensitivity
def plaintext_key_sensitivity():
    numbers, letters = load_plaintexts()
    keys = load_keys()

    print("PLAINTEXT SENSITIVITY TEST")
    for data_type, dataset in [("Letters", letters), ("Numbers", numbers)]:
            print(f"\n{data_type} with key {keys[0]}")
            for i in range(len(dataset) - 1):
                pt1 = dataset[i]
                pt2 = dataset[i + 1]

                cipher1 = des_encrypt(keys[0], pt1)
                cipher2 = des_encrypt(keys[0], pt2)

                total_bits = len(cipher1) * 8
                diff_bits = bit_difference(cipher1, cipher2)
                percent_diff = (diff_bits / total_bits) * 100

                print(f"Plaintext 1: {pt1} -> Ciphertext 1: {cipher1.hex().upper()}")
                print(f"Plaintext 2: {pt2} -> Ciphertext 2: {cipher2.hex().upper()}")
                print(f"Different bits: {diff_bits}/{total_bits} ({percent_diff:.2f}%)")

    print("\nKEY SENSITIVITY TEST")
    for pt in letters + numbers:
        cipher1 = des_encrypt(keys[0], pt)
        cipher2 = des_encrypt(keys[1], pt)

        total_bits = len(cipher1) * 8
        diff_bits = bit_difference(cipher1, cipher2)
        percent_diff = (diff_bits / total_bits) * 100

        print(f"\nPlaintext: {pt}")
        print(f"Key 1: {keys[0]} -> Ciphertext: {cipher1.hex().upper()}")
        print(f"Key 2: {keys[1]} -> Ciphertext: {cipher2.hex().upper()}")
        print(f"Different bits: {diff_bits}/{total_bits} ({percent_diff:.2f}%)")

if __name__ == "__main__":
    plaintext_key_sensitivity()