from algorithms.whirlpool_cipher import WhirlpoolCipher
from utils.helpers import whirlpool_pad

def whirlpool_hash(message: bytes) -> bytes:

    # Padding
    padded = whirlpool_pad(message)

    H = bytearray(64)
    whirlpool_cipher = WhirlpoolCipher()

    for i in range(0, len(padded), 64):
        block = padded[i:i+64]

        # Encrypt with key as H
        C = whirlpool_cipher.encrypt(block, H)
        # XOR with C, H and 
        H = bytearray([C[j] ^ block[j] ^ H[j] for j in range(64)])

    return bytes(H)