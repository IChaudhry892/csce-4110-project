import aes_encryption
from aes_encryption import encrypt, decrypt, convert_to_bytes, zero_pad, print_block_matrices
from des_encryption import des_encrypt, load_keys, load_plaintexts, bit_difference

import sys
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
    
def run_aes_plaintext_sensitivity_test(keys, numbers, letters, display_blocks=False):
    print("\n=== AES PLAINTEXT SENSITIVITY TEST ===")

    # Use the first key for testing
    aes_key = pad_key_for_aes(keys[0]).encode("utf-8")
    print(f"\nUsing AES Key: {aes_key}")

    for data_type, dataset in [("With Number Plaintexts", numbers), ("With Letter Plaintexts", letters)]:
        print(f"\n--- {data_type} ---\n")
        for i in range(len(dataset) - 1):
            if data_type == "With Number Plaintexts":
                plaintext1 = int(dataset[i])
                plaintext2 = int(dataset[i + 1])
            else:
                plaintext1 = dataset[i]
                plaintext2 = dataset[i + 1]

            ciphertext1, data_type_enc1 = encrypt(plaintext1, key=aes_key)
            ciphertext2, data_type_enc2 = encrypt(plaintext2, key=aes_key)

            diff_bits = bit_difference(ciphertext1, ciphertext2)
            total_bits = len(ciphertext1) * 8
            percent_diff = (diff_bits / total_bits) * 100
            
            print(f"Plaintext {i + 1}: {plaintext1} -> Ciphertext (hex): {ciphertext1.hex()}")
            if display_blocks:
                print(f" Plaintext {i + 1} blocks:")
                original_bytes, _ = convert_to_bytes(plaintext1)
                padded_original = zero_pad(original_bytes)
                print_block_matrices(padded_original)

                print(f" Ciphertext {i + 1} blocks:")
                print_block_matrices(ciphertext1)
            print(f"Plaintext {i + 2}: {plaintext2} -> Ciphertext (hex): {ciphertext2.hex()}")
            if display_blocks:
                print(f" Plaintext {i + 2} blocks:")
                original_bytes, _ = convert_to_bytes(plaintext2)
                padded_original = zero_pad(original_bytes)
                print_block_matrices(padded_original)

                print(f" Ciphertext {i + 2} blocks:")
                print_block_matrices(ciphertext2)
            print(f"Different bits: {diff_bits}/{total_bits} ({percent_diff:.2f}%)")

def run_aes_key_sensitivity_test(keys, numbers, letters, display_blocks=False):
    print("\n=== AES KEY SENSITIVITY TEST ===")

    # Use the first plaintexts for testing
    test_number = int(numbers[0])
    test_letter = letters[0]
    plaintexts = [test_number, test_letter]
    print(f"\nUsing Test Number Plaintext: {test_number}")
    print(f"Using Test Letter Plaintext: {test_letter}")

    for plaintext in plaintexts:
        print(f"\n--- With Plaintext: {plaintext} ---\n")
        ciphertexts = []
        for i, key in enumerate(keys):
            aes_key = pad_key_for_aes(key).encode("utf-8")
            ciphertext, data_type = encrypt(plaintext, key=aes_key)
            ciphertexts.append(ciphertext)
            print(f"Key {i + 1}: {key} -> Ciphertext (hex): {ciphertext.hex()}")

            if display_blocks:
                print(" Original plaintext blocks:")
                original_bytes, _ = convert_to_bytes(plaintext)
                padded_original = zero_pad(original_bytes)
                print_block_matrices(padded_original)

                print(" Ciphertext blocks:")
                print_block_matrices(ciphertext)

        # Compare ciphertexts from different keys
        for i in range(len(ciphertexts) - 1):
            c1 = ciphertexts[i]
            c2 = ciphertexts[i + 1]
            diff_bits = bit_difference(c1, c2)
            total_bits = len(c1) * 8
            percent_diff = (diff_bits / total_bits) * 100
            print(f"Different bits: {diff_bits}/{total_bits} ({percent_diff:.2f}%)")
    print()

def run_des_plaintext_sensitivity_test(keys, numbers, letters):
    print("\nDES PLAINTEXT SENSITIVITY TEST")
    key = keys[0]

    for data_type, dataset in [("Letters", letters), ("Numbers", numbers)]:
        print(f"\n--- {data_type} ---")
        for i in range(len(dataset) - 1):
            pt1, pt2 = dataset[i], dataset[i + 1]

            c1 = des_encrypt(key, pt1)
            c2 = des_encrypt(key, pt2)

            diff_bits = bit_difference(c1, c2)
            total_bits = len(c1) * 8
            percent_diff = (diff_bits / total_bits) * 100

            print(f"\nPlaintext 1: {pt1} -> Ciphertext 1: {c1.hex().upper()}")
            print(f"Plaintext 2: {pt2} -> Ciphertext 2: {c2.hex().upper()}")
            print(f"Different bits: {diff_bits}/{total_bits} ({percent_diff:.2f}%)")

def run_des_key_sensitivity_test(keys, numbers, letters):
    print("\nDES KEY SENSITIVITY TEST")
    for pt in letters + numbers:
        c1 = des_encrypt(keys[0], pt)
        c2 = des_encrypt(keys[1], pt)
        diff_bits = bit_difference(c1, c2)
        total_bits = len(c1) * 8
        percent_diff = (diff_bits / total_bits) * 100
        print(f"\nPlaintext: {pt}")
        print(f"Key 1: {keys[0]} -> Ciphertext: {c1.hex().upper()}")
        print(f"Key 2: {keys[1]} -> Ciphertext: {c2.hex().upper()}")
        print(f"Different bits: {diff_bits}/{total_bits} ({percent_diff:.2f}%)")

if __name__ == "__main__":
    keys = load_list_from_file(KEYS_FILE)
    numbers = load_list_from_file(NUMBERS_FILE)
    letters = load_list_from_file(LETTERS_FILE)
    print("Loaded Keys:", keys)
    print("Loaded Numbers:", numbers)
    print("Loaded Letters:", letters)

    if "--run-des-tests" in sys.argv:
        run_des_plaintext_sensitivity_test(keys, numbers, letters)
        run_des_key_sensitivity_test(keys, numbers, letters)
        sys.exit(0)
    
    if "--run-aes-tests-blocks" in sys.argv:
        run_aes_plaintext_sensitivity_test(keys, numbers, letters, display_blocks=True)
        run_aes_key_sensitivity_test(keys, numbers, letters, display_blocks=True)
        sys.exit(0)
    elif "--run-aes-tests" in sys.argv:
        run_aes_plaintext_sensitivity_test(keys, numbers, letters)
        run_aes_key_sensitivity_test(keys, numbers, letters)
        sys.exit(0)

    run_aes_plaintext_sensitivity_test(keys, numbers, letters)
    run_aes_key_sensitivity_test(keys, numbers, letters)

    run_des_plaintext_sensitivity_test(keys, numbers, letters)
    run_des_key_sensitivity_test(keys, numbers, letters)