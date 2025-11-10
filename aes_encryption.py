from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys

# 1. Generate a random 16-byte key for AES or use a fixed key
# KEY = get_random_bytes(16)
KEY = b"ThisIsA16ByteKey"

def zero_pad(data_bytes):
    """ Pads data with zero bytes to make its length a multiple of 16 """
    padding_needed = 16 - (len(data_bytes) % 16)
    if padding_needed == 16: # No padding needed
        return data_bytes
    return data_bytes + b"\x00" * padding_needed

def zero_unpad(data_bytes):
    """ Removes zero padding """
    return data_bytes.rstrip(b"\x00")

def convert_to_bytes(data):
    """ Converts the input data to bytes if it is not already """
    if isinstance(data, str):
        return data.encode("utf-8"), "str"
    elif isinstance(data, int):
        # Uses length of 8 bytes for integer representation
        return data.to_bytes(8, byteorder='big'), "int"
    else:
        raise TypeError("Unsupported data type for conversion to bytes")

def convert_from_bytes(data_bytes, data_type):
    """ Converts decrypted bytes back to the specified data type """
    if data_type == "str":
        return data_bytes.decode("utf-8")
    elif data_type == "int":
        return int.from_bytes(data_bytes, byteorder='big')
    else:
        raise TypeError("Unsupported data type for conversion from bytes")

def encrypt(plaintext, key=KEY):
    """ Encrypts the given plaintext using AES in EAX mode """
    # 2. Create a new AES cipher object for encryption in EAX mode
    data_bytes, data_type = convert_to_bytes(plaintext)

    padded = zero_pad(data_bytes)
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded)

    return ciphertext, data_type

def decrypt(ciphertext, data_type, key=KEY, test_params=None):
    """ Decrypts the given ciphertext using AES in EAX mode """
    # 3. Create a new AES cipher object for decryption using the same nonce
    cipher = AES.new(key, AES.MODE_ECB)
    padded_decrypted = cipher.decrypt(ciphertext)
    decrypted_bytes = zero_unpad(padded_decrypted)
    
    return convert_from_bytes(decrypted_bytes, data_type)

def split_blocks(data_bytes, block_size=16):
    """ Splits data bytes into blocks of specified size """
    return [data_bytes[i:i+block_size] for i in range(0, len(data_bytes), block_size)]

def print_block_matrix(block, matrix_size=4):
    """ Prints a single block as a 4x4 matrix """
    for r in range (matrix_size):
        row = block[r::matrix_size]
        print(" " + " ".join(f"{b:02x}" for b in row))
    print()

def print_block_matrices(data_bytes):
    """ Prints all blocks of a given data bytes as 4x4 matrices """
    blocks = split_blocks(data_bytes)
    for i, block in enumerate(blocks):
        print(f" Block {i}:")
        print_block_matrix(block)
    
def run_tests():
    """ Runs a series of tests to validate encryption and decryption """
    print("Running AES encryption/decryption tests...\n")

    tests = [
        ("No tamper (Control)", {}),
    ]

    for test_name, test_params in tests:
        print(f"--- Running test: {test_name}")
        message = "Ruh-roh Raggy! Ratch rout ror rat rar!"
        print(f"Original message: {message} (type: {type(message).__name__})")
        # Print blocks of original message
        print(" Original message blocks:")
        original_bytes, _ = convert_to_bytes(message)
        padded_original = zero_pad(original_bytes)
        print_block_matrices(padded_original)

        ciphertext, data_type = encrypt(message)
        print(f"\nData type: {data_type}")
        print(f"Ciphertext (hex): {ciphertext.hex()}")
        print(f"Key (hex): {KEY.hex()}")
        # Print blocks of ciphertext
        print("Ciphertext blocks:")
        print_block_matrices(ciphertext)

        decrypted_message = decrypt(ciphertext, data_type, test_params=test_params)
        print(f"Decrypted message: {decrypted_message} (type: {type(decrypted_message).__name__})")
        # Print blocks of decrypted message
        print(" Decrypted message blocks:")
        decrypted_bytes, _ = convert_to_bytes(decrypted_message)
        padded_decrypted = zero_pad(decrypted_bytes)
        print_block_matrices(padded_decrypted)

        print(f"Test: {test_name} completed.\n")

if __name__ == "__main__":
    # RUN TESTS
    if '--run-tests' in sys.argv:
        run_tests()
        sys.exit(0)

    # EXAMPLE USAGE
    message = input("Enter message or number (int) to encrypt: ")
    if message.isdigit():
        message = int(message)

    # Print blocks of original message
    print("\n Original message blocks:")
    original_bytes, _ = convert_to_bytes(message)
    padded_original = zero_pad(original_bytes)
    print_block_matrices(padded_original)

    ciphertext, data_type = encrypt(message)
    print(f"\nData type: {data_type}")
    print(f"Ciphertext (hex): {ciphertext.hex()}")

    # Print blocks of ciphertext
    print("Ciphertext blocks:")
    print_block_matrices(ciphertext)

    decrypted_message = decrypt(ciphertext, data_type)
    print(f"Decrypted message: {decrypted_message} (type: {type(decrypted_message).__name__})")

    # Print blocks of decrypted message
    print(" Decrypted message blocks:")
    decrypted_bytes, _ = convert_to_bytes(decrypted_message)
    padded_decrypted = zero_pad(decrypted_bytes)
    print_block_matrices(padded_decrypted)
