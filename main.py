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
