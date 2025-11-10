import aes_encryption
from aes_encryption import encrypt, decrypt, convert_to_bytes, zero_pad, print_block_matrices

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_FILE = os.path.join(BASE_DIR, "data", "keys.txt")
NUMBERS_FILE = os.path.join(BASE_DIR, "data", "plaintexts", "numbers.txt")
LETTERS_FILE = os.path.join(BASE_DIR, "data", "plaintexts", "letters.txt")

def load_list_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]
    
def pad_key_for_aes(key_str):
    """ Pads the key string with zeros to make it 16 bytes long """
    return key_str.ljust(16, "0")
    
def run_plaintext_sensitivity_test(keys, numbers, letters):
    print("\n=== PLAINTEXT SENSITIVITY TEST ===")

    # Use the first key for testing
    des_key = keys[0].encode("utf-8")
    aes_key = pad_key_for_aes(keys[0]).encode("utf-8")

    print(f"\nUsing DES Key: {des_key}")
    print(f"Using AES Key: {aes_key}\n")
    print("=== AES Plaintext Sensitivity Test with Numbers:")
    for number in numbers:
        plaintext = int(number)
        print(f"Original Number: {plaintext}")

        print(" Original message blocks:")
        original_bytes, _ = convert_to_bytes(plaintext)
        padded_original = zero_pad(original_bytes)
        print_block_matrices(padded_original)

        ciphertext, data_type = encrypt(plaintext, key=aes_key)
        print(f"Ciphertext (hex): {ciphertext.hex()}")
        print(" Ciphertext blocks:")
        print_block_matrices(ciphertext)

    print("=== AES Plaintext Sensitivity Test with Letters:")
    for letter in letters:
        plaintext = letter
        print(f"Original Letter: {plaintext}")

        print(" Original message blocks:")
        original_bytes, _ = convert_to_bytes(plaintext)
        padded_original = zero_pad(original_bytes)
        print_block_matrices(padded_original)

        ciphertext, data_type = encrypt(plaintext, key=aes_key)
        print(f"Ciphertext (hex): {ciphertext.hex()}")
        print(" Ciphertext blocks:")
        print_block_matrices(ciphertext)

if __name__ == "__main__":
    keys = load_list_from_file(KEYS_FILE)
    numbers = load_list_from_file(NUMBERS_FILE)
    letters = load_list_from_file(LETTERS_FILE)
    print("Loaded Keys:", keys)
    print("Loaded Numbers:", numbers)
    print("Loaded Letters:", letters)

    run_plaintext_sensitivity_test(keys, numbers, letters)