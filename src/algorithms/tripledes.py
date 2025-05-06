from utils.des_helpers import *
from utils.helpers import *
from algorithms.base import CryptoAlgorithm
from algorithms.des import DES
import hashlib
class TripleDES(CryptoAlgorithm):
    def __init__(self):
        super().__init__()
        self.des = DES()

    def mutate_key(self, original_key: str, seed: int) -> str:
        """
        Mutate the original key using a seed value.
        Args:
            original_key (str): The original key to mutate (56 bits)
            seed (int): The seed value to use for mutation
        Returns:
            str: The mutated key (56 bits)
        """
        data = original_key + str(seed)
        hashed = hashlib.md5(data.encode()).hexdigest().upper()
        return hashed[:16]  # Return the first 16 characters of the hash

    def encrypt(self, plaintext: str, k1: str, k2: str, k3: str = None, print_round_text=False) -> str:
        """
        Encrypt plaintext using 3DES (EDE: Encrypt-Decrypt-Encrypt)
        Args:
            plaintext (str): The plaintext to encrypt (64 bits)
            k1 (str): First key to encrypt (56 bits)
            k2 (str): Second key to decrypt (56 bits)
            k3 (str): Third key to encrypt (56 bits) (optional, if None, k1 is used)
            print_round_text (bool): If True, print the round text for each round
        Returns:
            str: The encrypted ciphertext (64 bits)
        """
        if k3 is None:
            k3 = k1  # 2-key mode

        # Step 1: Encrypt with K1
        step1 = self.des.encrypt(plaintext, k1, print_round_text)
        # Step 2: Decrypt with K2
        step2 = self.des.decrypt(step1, k2, print_round_text)
        # Step 3: Encrypt with K3
        ciphertext = self.des.encrypt(step2, k3, print_round_text)

        return ciphertext

    def decrypt(self, ciphertext: str, k1: str, k2: str, k3: str = None, print_round_text=False) -> str:
        """
        Decrypt ciphertext using 3DES (EDE: Decrypt-Encrypt-Decrypt)
        Args:
            ciphertext (str): The ciphertext to decrypt (64 bits)
            k1 (str): First key to decrypt (56 bits)
            k2 (str): Second key to encrypt (56 bits)
            k3 (str): Third key to decrypt (56 bits) (optional, if None, k1 is used)
            print_round_text (bool): If True, print the round text for each round
        Returns:
            str: The decrypted plaintext (64 bits)
        """
        if k3 is None:
            k3 = k1  # 2-key mode

        # Step 1: Decrypt with K3
        step1 = self.des.decrypt(ciphertext, k3, print_round_text)
        # Step 2: Encrypt with K2
        step2 = self.des.encrypt(step1, k2, print_round_text)
        # Step 3: Decrypt with K1
        plaintext = self.des.decrypt(step2, k1, print_round_text)

        return plaintext