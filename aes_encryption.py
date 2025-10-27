from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

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

def encrypt(plaintext):
    """ Encrypts the given plaintext using AES in EAX mode """
    # 2. Create a new AES cipher object for encryption in EAX mode
    data_bytes, data_type = convert_to_bytes(plaintext)
    cipher = AES.new(KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data_bytes)

    return nonce, ciphertext, tag, data_type

def decrypt(nonce, ciphertext, tag, data_type):
    """ Decrypts the given ciphertext using AES in EAX mode """
    # TESTING ERROR HANDLING BY MODIFYING CIPHERTEXT
    # ciphertext = bytearray(ciphertext)
    # ciphertext[0] ^= 1  # flip one bit
    # ciphertext = bytes(ciphertext)

    # TESTING ERROR HANDLING BY MODIFYING TAG
    # tag = bytearray(tag)
    # tag[0] ^= 1  # flip one bit
    # tag = bytes(tag)

    # TESTING ERROR HANDLING BY USING A DIFFERENT KEY
    # key = get_random_bytes(16)

    # 3. Create a new AES cipher object for decryption using the same nonce
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    decrypted_bytes = cipher.decrypt(ciphertext)

    # 4. Verify the integrity of the message using the tag
    try:
        cipher.verify(tag)
        print("SUCCESS: The message is authentic")
        return convert_from_bytes(decrypted_bytes, data_type)
    except ValueError: # If the tag does not match
        print("ERROR: Key incorrect or message corrupted")
        return None
    
if __name__ == "__main__":
    # EXAMPLE USAGE
    message = input("Enter message or number (int) to encrypt: ")
    if message.isdigit():
        message = int(message)

    nonce, ciphertext, tag, data_type = encrypt(message)
    print(f"\nData type: {data_type}")
    print(f"Ciphertext (hex): {ciphertext.hex()}")

    decrypted_message = decrypt(nonce, ciphertext, tag, data_type)
    print(f"Decrypted message: {decrypted_message} (type: {type(decrypted_message).__name__})\n")