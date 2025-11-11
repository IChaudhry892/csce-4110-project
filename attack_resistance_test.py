from aes_encryption import encrypt, decrypt, convert_to_bytes, zero_pad, print_block_matrices, pad_key_for_aes

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_FILE = os.path.join(BASE_DIR, "data", "keys.txt")

PACKETS_DIR = os.path.join(BASE_DIR, "data", "packets")
PACKETS_5MB_DIR = os.path.join(PACKETS_DIR, "5mb")
PACKETS_15MB_DIR = os.path.join(PACKETS_DIR, "15mb")
PACKETS_25MB_DIR = os.path.join(PACKETS_DIR, "25mb")
PACKETS_35MB_DIR = os.path.join(PACKETS_DIR, "35mb")
PACKETS_45MB_DIR = os.path.join(PACKETS_DIR, "45mb")

PACKETS_5MB_FILES = sorted([
    os.path.join(PACKETS_5MB_DIR, filename) for filename in os.listdir(PACKETS_5MB_DIR)
], reverse=True)
PACKETS_15MB_FILES = sorted([
    os.path.join(PACKETS_15MB_DIR, filename) for filename in os.listdir(PACKETS_15MB_DIR)
], reverse=True)
PACKETS_25MB_FILES = sorted([
    os.path.join(PACKETS_25MB_DIR, filename) for filename in os.listdir(PACKETS_25MB_DIR)
], reverse=True)
PACKETS_35MB_FILES = sorted([
    os.path.join(PACKETS_35MB_DIR, filename) for filename in os.listdir(PACKETS_35MB_DIR)
], reverse=True)
PACKETS_45MB_FILES = sorted([
    os.path.join(PACKETS_45MB_DIR, filename) for filename in os.listdir(PACKETS_45MB_DIR)
], reverse=True)

SAVED_DIR = os.path.join(BASE_DIR, "data", "encrypted_packets")
os.makedirs(SAVED_DIR, exist_ok=True)

def load_list_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]
    
def read_binary_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()
    
def write_binary_file(file_path, data_bytes):
    with open(file_path, 'wb') as f:
        f.write(data_bytes)
    
def run_aes_attack_resistance_test():
    pass

if __name__ == "__main__":
    keys = load_list_from_file(KEYS_FILE)
    print("Loaded Keys:", keys)

    if "--run-aes-tests" in sys.argv:
        run_aes_attack_resistance_test()
        sys.exit(0)

    run_aes_attack_resistance_test()