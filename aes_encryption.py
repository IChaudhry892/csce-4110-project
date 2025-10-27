from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# 1. Generate a random 16-byte key for AES or use a fixed key
# key = get_random_bytes(16)
key = b"ThisIsA16ByteKey"

def encrypt(plaintext):
    """ Encrypts the given plaintext using AES in EAX mode """
    # 2. Create a new AES cipher object for encryption in EAX mode
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("ascii"))

    return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag):
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
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_bytes = cipher.decrypt(ciphertext)

    # 4. Verify the integrity of the message using the tag
    try:
        cipher.verify(tag)
        print("SUCCESS: The message is authentic")
        return decrypted_bytes.decode("ascii")
    except ValueError: # If the tag does not match
        print("ERROR: Key incorrect or message corrupted")
        return None
    
if __name__ == "__main__":
    # EXAMPLE USAGE
    nonce, ciphertext, tag = encrypt(input("Enter message to encrypt: "))
    print(f"Ciphertext (hex): {ciphertext.hex()}")

    decrypted_message = decrypt(nonce, ciphertext, tag)
    print(f"Decrypted message: {decrypted_message}")