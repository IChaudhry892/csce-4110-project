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

    print("=== AES Plaintext Sensitivity Test with Number Plaintexts:")
    for number in numbers:
        plaintext = int(number)
        print(f"Using Original Number Plaintext: {plaintext}")

        print(" Original plaintext blocks:")
        original_bytes, _ = convert_to_bytes(plaintext)
        padded_original = zero_pad(original_bytes)
        print_block_matrices(padded_original)

        ciphertext, data_type = encrypt(plaintext, key=aes_key)
        print(f"Ciphertext (hex): {ciphertext.hex()}")
        print(" Ciphertext blocks:")
        print_block_matrices(ciphertext)

    print("=== AES Plaintext Sensitivity Test with Letter Plaintexts:")
    for letter in letters:
        plaintext = letter
        print(f"Using Original Letter Plaintext: {plaintext}")

        print(" Original plaintext blocks:")
        original_bytes, _ = convert_to_bytes(plaintext)
        padded_original = zero_pad(original_bytes)
        print_block_matrices(padded_original)

        ciphertext, data_type = encrypt(plaintext, key=aes_key)
        print(f"Ciphertext (hex): {ciphertext.hex()}")
        print(" Ciphertext blocks:")
        print_block_matrices(ciphertext)

def run_key_sensitivity_test(keys, numbers, letters):
    print("\n=== KEY SENSITIVITY TEST ===")

    # Use the first plaintexts for testing
    test_number = int(numbers[0])
    test_letter = letters[0]
    print(f"\nUsing Test Number Plaintext: {test_number}")
    print(f"Using Test Letter Plaintext: {test_letter}\n")

    print(f"=== AES Key Sensitivity Test with Number Plaintext: {test_number}")
    for key in keys:
        des_key = key.encode("utf-8")
        aes_key = pad_key_for_aes(key).encode("utf-8")
        print(f"Using DES Key: {des_key}")
        print(f"Using AES Key: {aes_key}")

        print(" Original plaintext blocks:")
        original_bytes, _ = convert_to_bytes(test_number)
        padded_original = zero_pad(original_bytes)
        print_block_matrices(padded_original)

        ciphertext, data_type = encrypt(test_number, key=aes_key)
        print(f"Ciphertext (hex): {ciphertext.hex()}")
        print(" Ciphertext blocks:")
        print_block_matrices(ciphertext)

    print(f"=== AES Key Sensitivity Test with Letter Plaintext: {test_letter}")
    for key in keys:
        aes_key = pad_key_for_aes(key).encode("utf-8")
        print(f"Using AES Key: {aes_key}")

        print(" Original plaintext blocks:")
        original_bytes, _ = convert_to_bytes(test_letter)
        padded_original = zero_pad(original_bytes)
        print_block_matrices(padded_original)

        ciphertext, data_type = encrypt(test_letter, key=aes_key)
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
    run_key_sensitivity_test(keys, numbers, letters)