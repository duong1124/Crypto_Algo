from utils.des_helpers import *
from utils.helpers import *
from algorithms.base import CryptoAlgorithm

class DES(CryptoAlgorithm):
    def __init__(self, key_size: int = 56):
        super().__init__()
        self.key_size = key_size

    def encrypt(self, plaintext: str, key: str, print_round_text = False) -> str:
        """Encrypt the plaintext using the DES algorithm.
        Args:
            plaintext (str): The plaintext to encrypt (64 bits)
            key (str): The key to encrypt the plaintext with (56 bits)
            print_round_text (bool): If True, print the round text for each round
        Returns:
            str: The encrypted ciphertext (64 bits)
        """
        permuted_plaintext = des_permute(plaintext, des_initial_permutation, 64)
        print(f"After initial permutation: {bin2hex(permuted_plaintext)}")
        left, right = split_half(permuted_plaintext)

        # Generate the 16 keys for each round   
        keys = des_key_generation(key)

        for round in range(16):
            left, right = des_mixer(left, right, keys[round])
            if round != 15:
                left, right = swap_half(left, right)
            if print_round_text:
                print(f"Round {round + 1}: L: {bin2hex(left)}, R: {bin2hex(right)}, Key: {bin2hex(keys[round])}")

        combined = des_combine(left, right)
        permuted_ciphertext = des_permute(combined, des_final_permutation, 64)
        return permuted_ciphertext
    
    def decrypt(self, ciphertext: str, key: str, print_round_text = False) -> str:
        """Decrypt the ciphertext using the DES algorithm.
        Args:
            ciphertext (str): The ciphertext to decrypt (64 bits)
            key (str): The key to decrypt the ciphertext with (56 bits)
            print_round_text (bool): If True, print the round text for each round
        Returns:
            str: The decrypted plaintext (64 bits)
        """
        permuted_ciphertext = des_permute(ciphertext, des_initial_permutation, 64)
        print(f"After initial permutation: {bin2hex(permuted_ciphertext)}")
        left, right = split_half(permuted_ciphertext)

        # Generate the 16 keys for each round
        keys = des_key_generation(key)
        keys.reverse()
        for round in range(16):
            left, right = des_mixer(left, right, keys[round])
            if round != 15:
                left, right = swap_half(left, right)
            if print_round_text:
                print(f"Round {round + 1}: L: {bin2hex(left)}, R: {bin2hex(right)}, Key: {bin2hex(keys[round])}")
        
        combined = des_combine(left, right)
        permuted_plaintext = des_permute(combined, des_final_permutation, 64)
        return permuted_plaintext