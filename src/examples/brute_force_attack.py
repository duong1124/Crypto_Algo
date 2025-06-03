import time
from typing import Tuple, Optional  
from utils import text_to_binary, binary_to_text, hex2bin, bin2hex

class BruteForceAttack():
    """
    Class to perform brute force attack on a generic algorithm (DES, 3DES, AES, ...).
    """
    def __init__(self, algo):
        self.algo = algo

    def generate_simple_test_case(self) -> Tuple[str, str, str]:
        """
        Generate a small test case with plaintext, key, and ciphertext.
        This should be in limitation of personal computer. (which i haven't known yet)
        """
        pass 

    def generate_test_case(self) -> Tuple[str, str, str]:
        """
        Generate a test case with plaintext, key, and ciphertext.
        Returns: (plaintext, key, ciphertext)
        """
        # Use a simple test case
        plaintext = "123456ABCD132536"
        key = "AABB09182736CCDD"  # 8 bytes = 64 bits (56 bits effective)
        ciphertext = self.algo.encrypt(hex2bin(plaintext), hex2bin(key))
        return plaintext, key, ciphertext

    def _brute_force_attack(self, ciphertext: str, known_plaintext: str, max_attempts: int = 1000) -> Optional[str]:
        """
        Attempt to find the key through brute force.
        Args:
            ciphertext: The encrypted text
            known_plaintext: The original plaintext
            max_attempts: Maximum number of keys to try
        Returns:
            The found key if successful, None otherwise
        """
        start_time = time.time()

        for i in range(max_attempts):
            test_key = f"TEST{i:04d}".ljust(8)  # Pad to 8 bytes
            try:
                decrypted = self.algo.decrypt(ciphertext, test_key)
                if decrypted == known_plaintext:
                    end_time = time.time()
                    print(f"\nKey found after {i+1} attempts!")
                    print(f"Time taken: {end_time - start_time:.2f} seconds")
                    return test_key
            except Exception as e:
                continue

            # Print progress every 100 attempts
            if (i + 1) % 100 == 0:
                print(f"Attempted {i+1} keys...")

        end_time = time.time()

        print(f"\nNo key found after {max_attempts} attempts")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        return None

    def demonstrate_brute_force(self, max_attempts: int):
        """
        Demonstrate a brute force attack on the algorithm.
        """
        print("Generating test case...")
        plaintext, original_key, ciphertext = self.generate_test_case()
        print(f"Plaintext: {plaintext}")
        print(f"Original Key: {original_key}")
        print(f"Ciphertext:\nAs binary {ciphertext}\nAs hexa{bin2hex(ciphertext)}")
        print(f"\nStarting brute force attack with {max_attempts} attempts...")
        found_key = self._brute_force_attack(ciphertext, plaintext, max_attempts=max_attempts)
        if found_key:
            print(f"\nSuccess! Found key: {found_key}")
            print(f"Original key was: {original_key}")
        else:
            print("\nAttack failed to find the key within the attempt limit")