import os
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 8

# load files 
def load_plaintexts(plaintext_path="data/plaintexts"):
    number_txt_file = os.path.join(plaintext_path, "numbers.txt")
    letter_txt_file = os.path.join(plaintext_path, "letters.txt")

    with open(number_txt_file, "r") as f:
        numbers = f.read().splitlines()
    
    with open(letter_txt_file, "r") as f:
        letters = f.read().splitlines()
    
    return numbers, letters

def load_keys(keys_path="data/keys.txt"):
    with open(keys_path, "r") as f:
        keys = f.read().splitlines()
    return keys

def des_encrypt(key, plaintext):
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    pad_txt = pad(plaintext.encode('utf-8'), BLOCK_SIZE)
    return cipher.encrypt(pad_txt)

def des_decrypt(key, ciphertext):
    cipher = DES.new(key.encode('utf-8'), DES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted, BLOCK_SIZE).decode('utf-8')

def bit_difference(cipher1, cipher2):
    diff = 0
    for b1, b2 in zip(cipher1, cipher2):
        diff += bin(b1 ^ b2).count("1")
    return diff