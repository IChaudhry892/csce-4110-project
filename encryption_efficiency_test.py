from aes_encryption import encrypt, convert_to_bytes, zero_pad, print_block_matrices, pad_key_for_aes
from des_encryption import des_encrypt, load_keys, load_plaintexts

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_FILE = os.path.join(BASE_DIR, "data", "keys.txt")

AUDIOS_DIR = os.path.join(BASE_DIR, "data", "files", "audios")
DOCUMENTS_DIR = os.path.join(BASE_DIR, "data", "files", "documents")
IMAGES_DIR = os.path.join(BASE_DIR, "data", "files", "images")

AUDIOS_FILES = sorted([
    os.path.join(AUDIOS_DIR, filename) for filename in os.listdir(AUDIOS_DIR)
], reverse=True)
DOCUMENTS_FILES = sorted([
    os.path.join(DOCUMENTS_DIR, filename) for filename in os.listdir(DOCUMENTS_DIR)
], reverse=True)
IMAGES_FILES = sorted([
    os.path.join(IMAGES_DIR, filename) for filename in os.listdir(IMAGES_DIR)
], reverse=True)

SAVED_DIR = os.path.join(BASE_DIR, "data", "encrypted_files")
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

def time_to_encrypt(data_bytes, key):
    start_time = time.time()
    ciphertext, _ = encrypt(data_bytes, key=key)
    end_time = time.time()
    return end_time - start_time, ciphertext

def run_group(file_label, file, key, category):
    print(f"--- Files of label: {file_label} ---\n")
    times = []
    # Encrypt the same file 10 times due to storage constraints
    for i in range(10):
        data_bytes = read_binary_file(file)
        elapsed_time, ciphertext = time_to_encrypt(data_bytes, key)
        times.append(elapsed_time)
        print(f"Run {i + 1} encryption time: {elapsed_time:.6f} seconds")

        if i == 9:  # On the last run, save the encrypted file
            category_dir = os.path.join(SAVED_DIR, category)
            os.makedirs(category_dir, exist_ok=True)
            out_path = os.path.join(category_dir, f"{file_label}_encrypted.bin")
            write_binary_file(out_path, ciphertext)
            print(f"Saved encrypted file to: {out_path}")

    average_encryption_time = sum(times) / len(times)
    print(f"\nAverage encryption time: {average_encryption_time:.6f} seconds\n")
    return average_encryption_time

def run_aes_efficiency_test(keys):
    print("\n=== ENCRYPTION EFFICIENCY TEST ===")
    # Use the first key for testing
    aes_key = pad_key_for_aes(keys[0]).encode("utf-8")
    print(f"Using AES Key: {aes_key}\n")

    results = {}
    results["1MB_audio"] = run_group("1MB_audio", AUDIOS_FILES[0], aes_key, "audios")
    results["10MB_audio"] = run_group("10MB_audio", AUDIOS_FILES[1], aes_key, "audios")
    results["100MB_audio"] = run_group("100MB_audio", AUDIOS_FILES[2], aes_key, "audios")

    results["1MB_document"] = run_group("1MB_document", DOCUMENTS_FILES[0], aes_key, "documents")
    results["10MB_document"] = run_group("10MB_document", DOCUMENTS_FILES[1], aes_key, "documents")
    results["100MB_document"] = run_group("100MB_document", DOCUMENTS_FILES[2], aes_key, "documents")

    results["1MB_image"] = run_group("1MB_image", IMAGES_FILES[0], aes_key, "images")
    results["10MB_image"] = run_group("10MB_image", IMAGES_FILES[1], aes_key, "images")
    results["100MB_image"] = run_group("100MB_image", IMAGES_FILES[2], aes_key, "images")

    print("=== AVERAGE ENCRYPTION TIME RESULTS ===")
    for file_label, average__encryption_time in results.items():
        print(f"{file_label}: {average__encryption_time:.6f} seconds")
    print()

def encrypt_time_des(data_bytes, key):
    from Crypto.Cipher import DES
    from Crypto.Util.Padding import pad
    
    key_bytes = key.encode('utf-8')[:8].ljust(8, b'0')
    des = DES.new(key_bytes, DES.MODE_ECB)
    padded = pad(data_bytes, 8)
    start_time = time.time()
    ciphertext = des.encrypt(padded)
    end_time = time.time()
    
    return end_time - start_time, ciphertext

def run_group_des(file_label, file, key, category):
    print(f"DES Encryption for: {file_label}\n")
    times = []

    for i in range(10):
        data_bytes = read_binary_file(file)
        elapsed_time, ciphertext = encrypt_time_des(data_bytes, key)
        times.append(elapsed_time)
        print(f"Run {i+1} encryption time: {elapsed_time:.6f} seconds")

        if i == 9:
            category_dir = os.path.join(SAVED_DIR, category)
            os.makedirs(category_dir, exist_ok=True)
            out_path = os.path.join(category_dir, f"{file_label}_des_encrypted.bin")
            write_binary_file(out_path, ciphertext)
            print(f"Saved DES encrypted file to: {out_path}")
        
    avg_encryption_time = sum(times) / len(times)
    print(f"\nAverage DES encryption time: {avg_encryption_time:.6f} seconds\n")

    return avg_encryption_time

def run_des_efficiency_test(keys):
    print("DES ENCRYPTION TEST")
    des_key = keys[0]
    print(f"Using DES key: {des_key}")

    results = {}
    results["1MB_audio"] = run_group_des("1MB_audio", AUDIOS_FILES[0], des_key, "audios")
    results["10MB_audio"] = run_group_des("10MB_audio", AUDIOS_FILES[1], des_key, "audios")
    results["100MB_audio"] = run_group_des("100MB_audio", AUDIOS_FILES[2], des_key, "audios")

    results["1MB_document"] = run_group_des("1MB_document", DOCUMENTS_FILES[0], des_key, "documents")
    results["10MB_document"] = run_group_des("10MB_document", DOCUMENTS_FILES[1], des_key, "documents")
    results["100MB_document"] = run_group_des("100MB_document", DOCUMENTS_FILES[2], des_key, "documents")

    results["1MB_image"] = run_group_des("1MB_image", IMAGES_FILES[0], des_key, "images")
    results["10MB_image"] = run_group_des("10MB_image", IMAGES_FILES[1], des_key, "images")
    results["100MB_image"] = run_group_des("100MB_image", IMAGES_FILES[2], des_key, "images")

    print("DES AVERAGE ENCRYPTION TIME RESULTS")
    for file_label, avg_time in results.items():
        print(f"{file_label}: {avg_time:.6f} seconds\n")

    return results

if __name__ == "__main__":
    keys = load_list_from_file(KEYS_FILE)
    print("Loaded Keys:", keys)
    print("Loaded AUDIOS_FILES:", AUDIOS_FILES)
    print("Loaded DOCUMENTS_FILES:", DOCUMENTS_FILES)
    print("Loaded IMAGES_FILES:", IMAGES_FILES)

    if "--run-aes-tests" in sys.argv:
        run_aes_efficiency_test(keys)
        sys.exit(0)

    if "--run-des-tests" in sys.argv:
        run_des_efficiency_test(keys)
        sys.exit(0)

    run_aes_efficiency_test(keys)
    run_des_efficiency_test(keys)