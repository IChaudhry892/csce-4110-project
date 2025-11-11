from aes_encryption import encrypt, decrypt, convert_to_bytes, zero_pad, print_block_matrices, pad_key_for_aes
from Crypto.Random import get_random_bytes

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
])
PACKETS_15MB_FILES = sorted([
    os.path.join(PACKETS_15MB_DIR, filename) for filename in os.listdir(PACKETS_15MB_DIR)
])
PACKETS_25MB_FILES = sorted([
    os.path.join(PACKETS_25MB_DIR, filename) for filename in os.listdir(PACKETS_25MB_DIR)
])
PACKETS_35MB_FILES = sorted([
    os.path.join(PACKETS_35MB_DIR, filename) for filename in os.listdir(PACKETS_35MB_DIR)
])
PACKETS_45MB_FILES = sorted([
    os.path.join(PACKETS_45MB_DIR, filename) for filename in os.listdir(PACKETS_45MB_DIR)
])

SAVED_DIR = os.path.join(BASE_DIR, "data", "encrypted_packets")
os.makedirs(SAVED_DIR, exist_ok=True)

TOTAL_TIME_SECONDS = 6 * 60  # 6 minutes total to crack all encrypted data
TIME_PER_PACKET = 14.4 # Seconds to spend on each packet file (assuming 25 total packets)

def load_list_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]
    
def read_binary_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()
    
def write_binary_file(file_path, data_bytes):
    with open(file_path, 'wb') as f:
        f.write(data_bytes)

def byte_match_fraction(data1: bytes, data2: bytes) -> float:
    """ Returns the fraction of bytes that match between two byte sequences """
    length_to_compare = min(len(data1), len(data2))
    if length_to_compare == 0:
        return 0.0
    matches = sum(1 for i in range(length_to_compare) if data1[i] == data2[i])
    return matches / length_to_compare

def simulate_aes_attack_on_single_ciphertext(ciphertext: bytes, original_plaintext: bytes, time_limit: float):
    """ Simulates an attack on AES ciphertext by attempting to decrypt with random keys """
    best_match_fraction = 0.0
    best_match_key = None
    attempts = 0
    start = time.perf_counter()
    deadline = start + time_limit

    while time.perf_counter() < deadline:
        attempts += 1
        candidate_key = get_random_bytes(16)
        candidate_plaintext = decrypt(ciphertext, data_type="bytes", key=candidate_key)
        match_fraction = byte_match_fraction(candidate_plaintext, original_plaintext)
        if match_fraction > best_match_fraction:
            best_match_fraction = match_fraction
            best_match_key = candidate_key
    
    elapsed = time.perf_counter() - start
    best_match_key_hex = best_match_key.hex() if best_match_key else None
    return best_match_fraction, best_match_key_hex, attempts, elapsed
    
def run_aes_attack_resistance_test(keys):
    print("\n=== AES ATTACK RESISTANCE TEST ===")
    # Use the first key for testing
    real_key = pad_key_for_aes(keys[0]).encode("utf-8")
    print(f"Using AES Key: {real_key}")

    packets_by_size = {}
    packets_by_size["5MB"] = PACKETS_5MB_FILES
    packets_by_size["15MB"] = PACKETS_15MB_FILES
    packets_by_size["25MB"] = PACKETS_25MB_FILES
    packets_by_size["35MB"] = PACKETS_35MB_FILES
    packets_by_size["45MB"] = PACKETS_45MB_FILES

    results = {}
    for size_label, packet_files in packets_by_size.items():
        if not packet_files:
            results[size_label] = []
            continue
        size_out_dir = os.path.join(SAVED_DIR, size_label)
        os.makedirs(size_out_dir, exist_ok=True)
        results[size_label] = []

        print(f"\n--- Testing Packets of Size: {size_label} ---")
        for packet_file in packet_files:
            basename = os.path.basename(packet_file)
            print(f"\nPacket: {basename}")

            original_data = read_binary_file(packet_file)
            ciphertext, _ = encrypt(original_data, key=real_key)
            out_path = os.path.join(size_out_dir, f"{basename}_encrypted.bin")
            write_binary_file(out_path, ciphertext)
            print(f"Saved encrypted packet to: {out_path} (size: {len(ciphertext)} bytes)")

            # Simulate attacker trying to crack this single ciphertext within TIME_PER_PACKET seconds
            best_fraction, best_key_hex, attempts, elapsed = simulate_aes_attack_on_single_ciphertext(
                ciphertext, original_data, TIME_PER_PACKET
            )

            results[size_label].append(best_fraction)
            print(f"Best matched fraction: {best_fraction:.6f}")
            print(f"Best matched key (hex): {best_key_hex}")
            print(f"Attempts: {attempts} in {elapsed:.3f} seconds")

    # Print decryption integrity result for each packet size
    print("\n=== DECRYPTION INTEGRITY RESULTS ===")
    for size_label, fractions in results.items():
        if fractions:
            average_fraction = sum(fractions) / len(fractions)
            print(f"{size_label}: average best matched fraction = {average_fraction*100:.6f}% over {len(fractions)} packets")
        else:
            print(f"{size_label}: No packets tested.")
    print()

if __name__ == "__main__":
    keys = load_list_from_file(KEYS_FILE)
    print("Loaded Keys:", keys)
    print("Loaded PACKETS_5MB_FILES:", PACKETS_5MB_FILES)
    print("Loaded PACKETS_15MB_FILES:", PACKETS_15MB_FILES)
    print("Loaded PACKETS_25MB_FILES:", PACKETS_25MB_FILES)
    print("Loaded PACKETS_35MB_FILES:", PACKETS_35MB_FILES)
    print("Loaded PACKETS_45MB_FILES:", PACKETS_45MB_FILES)
    if "--run-aes-test" in sys.argv:
        run_aes_attack_resistance_test(keys)
        sys.exit(0)

    run_aes_attack_resistance_test(keys)