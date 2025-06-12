import time
import statistics
from typing import Tuple, Optional
from utils import hex2bin, bin2hex

class TimingAttack:
    """
    Class to perform timing attack on a generic algorithm (DES, 3DES, AES, ...).
    Assumes the algorithm's key verification is vulnerable to timing differences.
    """
    def __init__(self, algo):
        self.algo = algo

    def generate_test_case(self) -> Tuple[str, str, str]:
        """
        Generate a test case with plaintext, key, and ciphertext.
        Returns: (plaintext, key, ciphertext)
        """
        plaintext = "123456ABCD132536"  # Same as BruteForceAttack
        key = "AABB09182736CCDD"   # 8 bytes = 64 bits (DES compatible)
        ciphertext = self.algo.encrypt(hex2bin(plaintext), hex2bin(key))
        return plaintext, key, ciphertext

    def _vulnerable_key_check(self, input_key: str, correct_key: str) -> bool:
        """
        Simulate a vulnerable key check that leaks timing information.
        Compares keys byte-by-byte, stopping at first mismatch.
        """
        input_bytes = hex2bin(input_key)
        correct_bytes = hex2bin(correct_key)
        if len(input_bytes) != len(correct_bytes):
            return False
        for i in range(len(input_bytes)):
            if input_bytes[i] != correct_bytes[i]:
                return False
            # Simulate small delay to amplify timing difference
            time.sleep(0.0001)
        return True

    def _timing_attack(self, ciphertext: str, plaintext: str, correct_key: str, max_attempts: int = 16) -> Optional[str]:
        """
        Perform timing attack to guess the key.
        Args:
            ciphertext: The encrypted text
            plaintext: The known plaintext
            correct_key: The key to attack (for simulation)
            max_attempts: Maximum bytes to guess
        Returns:
            The guessed key if successful, None otherwise
        """
        start_time = time.time()
        guessed_key = ""
        charset = "0123456789ABCDEF"  # Hex characters for key

        for position in range(min(max_attempts, 16)):  # Limit to 8 bytes (16 hex chars)
            print(f"Guessing byte {position // 2 + 1}...")
            times = {}

            # Try each character in charset
            for char in charset:
                test_key = guessed_key + char + "0" * (16 - len(guessed_key) - 1)
                measurements = []

                # Measure multiple times to reduce noise
                for _ in range(50):
                    start = time.perf_counter()
                    self._vulnerable_key_check(test_key, correct_key)
                    end = time.perf_counter()
                    measurements.append(end - start)

                # Compute average time
                times[char] = statistics.mean(measurements)

            # Select character with longest time (likely correct)
            best_char = max(times, key=times.get)
            guessed_key += best_char
            print(f"Guessed char: {best_char}, Current key: {guessed_key}")

            # Verify if guessed key is correct
            test_key = guessed_key + "0" * (16 - len(guessed_key))
            try:
                decrypted = self.algo.decrypt(ciphertext, hex2bin(test_key))
                if decrypted == hex2bin(plaintext):
                    end_time = time.time()
                    print(f"\nKey found after guessing {len(guessed_key)} chars!")
                    print(f"Time taken: {end_time - start_time:.2f} seconds")
                    return test_key
            except Exception:
                continue

        end_time = time.time()
        print(f"\nNo key found after guessing {max_attempts} chars")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        return None

    def demonstrate_timing_attack(self, max_attempts: int = 16):
        """
        Demonstrate a timing attack on the algorithm.
        """
        print("Generating test case...")
        plaintext, original_key, ciphertext = self.generate_test_case()
        print(f"Plaintext: {plaintext}")
        print(f"Original Key: {original_key}")
        print(f"Ciphertext:\nAs binary {ciphertext}\nAs hex {bin2hex(ciphertext)}")
        print(f"\nStarting timing attack with {max_attempts} chars...")
        found_key = self._timing_attack(ciphertext, plaintext, original_key, max_attempts)
        if found_key:
            print(f"\nSuccess! Found key: {found_key}")
            print(f"Original key was: {original_key}")
        else:
            print("\nAttack failed to find the key within the attempt limit")