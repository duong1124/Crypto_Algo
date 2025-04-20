from utils.des_helpers import *
from utils.helpers import *
from algorithms.base import CryptoAlgorithm

class DES(CryptoAlgorithm):
    def __init__(self, key_size: int = 56):
        super().__init__()
        self.key_size = key_size

    def encrypt(self, plaintext: str, key: str) -> str:
        """Encrypt the plaintext using the DES algorithm.
        Args:
            plaintext (str): The plaintext to encrypt (64 bits)
            key (str): The key to encrypt the plaintext with (56 bits)
        Returns:
            str: The encrypted ciphertext (64 bits)
        """
        permuted_plaintext = des_permute(plaintext, des_initial_permutation, 64)
        left, right = split_half(permuted_plaintext)

        # Generate the 16 keys for each round   
        keys = des_key_generation(key)

        for round in range(16):
            left, right = des_mixer(left, right, keys[round])
            if round != 15:
                left, right = swap_half(left, right)

        combined = des_combine(left, right)
        permuted_ciphertext = des_permute(combined, des_final_permutation, 64)
        return permuted_ciphertext
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt the ciphertext using the DES algorithm."""
        pass # TODO: Implement the decryption function
