import aes_encryption
from aes_encryption import encrypt, decrypt, convert_to_bytes, zero_pad, print_block_matrices

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_FILE = os.path.join(BASE_DIR, "data", "keys.txt")

AUDIOS_DIR = os.path.join(BASE_DIR, "data", "files", "audios")
AUDIOS_FILES = sorted([
    os.path.join(AUDIOS_DIR, filename) for filename in os.listdir(AUDIOS_DIR)
], reverse=True)

DOCUMENTS_DIR = os.path.join(BASE_DIR, "data", "files", "documents")
DOCUMENTS_FILES = sorted([
    os.path.join(DOCUMENTS_DIR, filename) for filename in os.listdir(DOCUMENTS_DIR)
], reverse=True)

IMAGES_DIR = os.path.join(BASE_DIR, "data", "files", "images")
IMAGES_FILES = sorted([
    os.path.join(IMAGES_DIR, filename) for filename in os.listdir(IMAGES_DIR)
], reverse=True)


def load_list_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]
    
def pad_key_for_aes(key_str):
    """ Pads the key string with zeros to make it 16 bytes long """
    return key_str.ljust(16, "0")

def run_efficiency_test(keys):
    print("\n=== ENCRYPTION EFFICIENCY TEST ===")

    # Use the first key for testing
    des_key = keys[0].encode("utf-8")
    aes_key = pad_key_for_aes(keys[0]).encode("utf-8")
    print(f"\nUsing DES Key: {des_key}")
    print(f"Using AES Key: {aes_key}\n")

    pass

if __name__ == "__main__":
    keys = load_list_from_file(KEYS_FILE)
    print("Loaded Keys:", keys)
    print("Loaded AUDIOS_FILES:", AUDIOS_FILES)
    print("Loaded DOCUMENTS_FILES:", DOCUMENTS_FILES)
    print("Loaded IMAGES_FILES:", IMAGES_FILES)
