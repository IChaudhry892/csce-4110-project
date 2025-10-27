from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys

# 1. Generate a random 16-byte key for AES or use a fixed key
# KEY = get_random_bytes(16)
KEY = b"ThisIsA16ByteKey"

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
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data_bytes)

    return nonce, ciphertext, tag, data_type

def decrypt(nonce, ciphertext, tag, data_type, key=KEY, test_params=None):
    """ Decrypts the given ciphertext using AES in EAX mode """

    # OPTIONAL: TESTING ERROR HANDLING BY USING A DIFFERENT KEY
    if test_params and test_params.get("use_different_key"):
        key = get_random_bytes(16)
        print("New key (hex):", key.hex())

    # 3. Create a new AES cipher object for decryption using the same nonce
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    # OPTIONAL: TESTING ERROR HANDLING BY MODIFYING CIPHERTEXT
    if test_params and test_params.get("modify_ciphertext"):
        ciphertext = bytearray(ciphertext)
        ciphertext[0] ^= 1  # flip one bit
        ciphertext = bytes(ciphertext)
        print("Modified ciphertext (hex):", ciphertext.hex())

    decrypted_bytes = cipher.decrypt(ciphertext)

    # OPTIONAL: TESTING ERROR HANDLING BY MODIFYING TAG
    if test_params and test_params.get("modify_tag"):
        tag = bytearray(tag)
        tag[0] ^= 1  # flip one bit
        tag = bytes(tag)
        print("Modified tag (hex):", tag.hex())

    # 4. Verify the integrity of the message using the tag
    try:
        cipher.verify(tag)
        print("SUCCESS: The message is authentic")
        return convert_from_bytes(decrypted_bytes, data_type)
    except ValueError: # If the tag does not match
        print("ERROR: Key incorrect or message corrupted")
        return None
    
def run_tests():
    """ Runs a series of tests to validate encryption and decryption """
    print("Running AES encryption/decryption tests...\n")

    tests = [
        ("No tamper (Control)", {}),
        ("Modify ciphertext", {"modify_ciphertext": True}),
        ("Modify tag", {"modify_tag": True}),
        ("Use different key", {"use_different_key": True}),
    ]

    for test_name, test_params in tests:
        print(f"--- Running test: {test_name}")
        message = "Ruh-roh Raggy!"
        nonce, ciphertext, tag, data_type = encrypt(message)
        print(f"\nData type: {data_type}")
        print(f"Ciphertext (hex): {ciphertext.hex()}")
        print(f"Tag (hex): {tag.hex()}")
        print(f"Key (hex): {KEY.hex()}")
        decrypted_message = decrypt(nonce, ciphertext, tag, data_type, test_params=test_params)
        print(f"Decrypted message: {decrypted_message} (type: {type(decrypted_message).__name__})")
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

    nonce, ciphertext, tag, data_type = encrypt(message)
    print(f"\nData type: {data_type}")
    print(f"Ciphertext (hex): {ciphertext.hex()}")

    decrypted_message = decrypt(nonce, ciphertext, tag, data_type)
    print(f"Decrypted message: {decrypted_message} (type: {type(decrypted_message).__name__})\n")