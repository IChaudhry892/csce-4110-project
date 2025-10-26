from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

# plain-texts
# 1234567890 & 1234567899
plaintext1 = b'1234567890'
plaintext2 = b'1234567899'

# two letter-plaintexts
# abcde-fghij & abcdefghii
letplaintext1 = b'abcde-fghij'
letplaintext2 = b'abcedfghii'

# key for both encryption algorithm
# 32568894
key = b'32568894'

# AES encryption/decryption

# DES encryption/decryption
def DES_ENC_DEC(key: bytes, plaintext: bytes):
    cipher = DES.new(key, DES.MODE_ECB)

    padded_text = pad(plaintext, DES.block_size)
    ciphertext = cipher.encrypt(padded_text)

    decipher = DES.new(key, DES.MODE_ECB)
    decrypted_padded = decipher.decrypt(ciphertext)
    decrypted = unpad(decrypted_padded, DES.block_size)

    return ciphertext.hex(), decrypted.decode()

if __name__ == "__main__":

    # DES ENCRYPT/DECRYPT
    cipher_hex, decrypted_text = DES_ENC_DEC(key, plaintext1)
    print("Ciphertext: ", cipher_hex)
    print("Decrypted: ", decrypted_text)