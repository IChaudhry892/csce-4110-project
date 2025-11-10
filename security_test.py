from aes_encryption import encrypt, decrypt, convert_to_bytes, zero_pad, print_block_matrices, pad_key_for_aes

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_FILE = os.path.join(BASE_DIR, "data", "keys.txt")

ENCRYPTED_DIR = os.path.join(BASE_DIR, "data", "encrypted_files")
AUDIOS_DIR = os.path.join(ENCRYPTED_DIR, "audios")
DOCUMENTS_DIR = os.path.join(ENCRYPTED_DIR, "documents")
IMAGES_DIR = os.path.join(ENCRYPTED_DIR, "images")

AUDIOS_FILES = sorted([
    os.path.join(AUDIOS_DIR, filename) for filename in os.listdir(AUDIOS_DIR)
], reverse=True)
DOCUMENTS_FILES = sorted([
    os.path.join(DOCUMENTS_DIR, filename) for filename in os.listdir(DOCUMENTS_DIR)
], reverse=True)
IMAGES_FILES = sorted([
    os.path.join(IMAGES_DIR, filename) for filename in os.listdir(IMAGES_DIR)
], reverse=True)

def load_list_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]
    
def read_binary_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def time_to_decrypt(ciphertext, data_type, key):
    start_time = time.time()
    decrypted_data = decrypt(ciphertext, data_type, key=key)
    end_time = time.time()
    return end_time - start_time

def run_group(file_label, file, key):
    print(f"--- Files of label: {file_label} ---\n")
    times = []
    # Decrypt the same file 10 times due to storage constraints
    for i in range(10):
        ciphertext = read_binary_file(file)
        elapsed_time = time_to_decrypt(ciphertext, data_type="bytes", key=key)
        times.append(elapsed_time)
        print(f"Run {i + 1} decryption time: {elapsed_time:.6f} seconds")
    average_decryption_time = sum(times) / len(times)
    print(f"Average decryption time for {file_label}: {average_decryption_time:.6f} seconds\n")
    return average_decryption_time
    
def run_aes_security_test(keys):
    print("\n=== DECRYPTION EFFICIENCY TEST ===")
    # Use the first key for testing
    aes_key = pad_key_for_aes(keys[0]).encode("utf-8")
    print(f"Using AES Key: {aes_key}\n")

    results = {}
    results["1MB_audio"] = run_group("1MB_audio", AUDIOS_FILES[0], aes_key)
    results["10MB_audio"] = run_group("10MB_audio", AUDIOS_FILES[1], aes_key)
    results["100MB_audio"] = run_group("100MB_audio", AUDIOS_FILES[2], aes_key)

    results["1MB_document"] = run_group("1MB_document", DOCUMENTS_FILES[0], aes_key)
    results["10MB_document"] = run_group("10MB_document", DOCUMENTS_FILES[1], aes_key)
    results["100MB_document"] = run_group("100MB_document", DOCUMENTS_FILES[2], aes_key)

    results["1MB_image"] = run_group("1MB_image", IMAGES_FILES[0], aes_key)
    results["10MB_image"] = run_group("10MB_image", IMAGES_FILES[1], aes_key)
    results["100MB_image"] = run_group("100MB_image", IMAGES_FILES[2], aes_key)

    print("=== AVERAGE DECRYPTION TIME RESULTS ===")
    for file_label, average__decryption_time in results.items():
        print(f"{file_label}: {average__decryption_time:.6f} seconds")
    print()
    
if __name__ == "__main__":
    keys = load_list_from_file(KEYS_FILE)
    print("Loaded Keys:", keys)
    print("Loaded AUDIOS_FILES:", AUDIOS_FILES)
    print("Loaded DOCUMENTS_FILES:", DOCUMENTS_FILES)
    print("Loaded IMAGES_FILES:", IMAGES_FILES)

    if "--run-aes-tests" in sys.argv:
        run_aes_security_test(keys)
        sys.exit(0)

    run_aes_security_test(keys)