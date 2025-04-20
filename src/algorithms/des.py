from utils.des_helpers import *
from utils.helpers import *
from algorithms.base import CryptoAlgorithm

class DES(CryptoAlgorithm):
    def __init__(self, key_size: int = 32):
        super().__init__()
        self.key_size = key_size
        self.generate_key()

    def encrypt(plaintext: str, key: str) -> str:
        """Encrypt the plaintext using the DES algorithm."""
        permuted_plaintext = des_permute(plaintext, des_initial_permutation, 64)
        left, right = des_split(permuted_plaintext, 32)
        for round in range(16):
            left, right = des_mixer(left, right, des_key_generation(key)[round])
            if round != 15:
                left, right = des_swapper(left + right)
        combined = des_combine(left, right)
        permuted_ciphertext = des_permute(combined, des_final_permutation, 64)
        return permuted_ciphertext
    
    def decrypt(ciphertext: str, key: str) -> str:
        """Decrypt the ciphertext using the DES algorithm."""
        permuted_ciphertext = des_permute(ciphertext, des_initial_permutation, 64)
        left, right = des_split(permuted_ciphertext, 32)
        for round in range(16):
            left, right = des_mixer(left, right, des_key_generation(key)[round])
            if round != 15:
                left, right = des_swapper(left + right)
        combined = des_combine(left, right)
        permuted_plaintext = des_permute(combined, des_final_permutation, 64)
        return permuted_plaintext
