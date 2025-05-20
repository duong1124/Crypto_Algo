import time
from typing import Tuple, Optional
from algorithms import DES
from utils import text_to_binary, binary_to_text, hex2bin, bin2hex

def generate_simple_test_case() -> Tuple[str, str, str]:
    """
    Generate a small test case with plaintext, key, and ciphertext.
    This should be in limitation of personal computer. (which i haven't known yet)
    """
    pass 

def generate_test_case() -> Tuple[str, str, str]:
    """
    Generate a test case with plaintext, key, and ciphertext.
    Returns: (plaintext, key, ciphertext)
    """
    # Use a simple test case
    plaintext = "123456ABCD132536"
    key = "AABB09182736CCDD"  # 8 bytes = 64 bits (56 bits effective)
    des = DES()
    ciphertext = des.encrypt(hex2bin(plaintext), hex2bin(key))
    return plaintext, key, ciphertext

def brute_force_attack(ciphertext: str, known_plaintext: str, max_attempts: int = 1000) -> Optional[str]:
    """
    Attempt to find the key through brute force.
    Args:
        ciphertext: The encrypted text
        known_plaintext: The original plaintext
        max_attempts: Maximum number of keys to try
    Returns:
        The found key if successful, None otherwise
    """
    des = DES()
    start_time = time.time()
    
    # In a real attack, we would try all possible 2^56 keys
    # For demonstration, we'll try a limited number of keys
    for i in range(max_attempts):
        # Generate a test key (in reality, this would be systematic)
        test_key = f"TEST{i:04d}".ljust(8)  # Pad to 8 bytes
        
        try:
            # Try to decrypt with this key
            decrypted = des.decrypt(ciphertext, test_key)
            
            # Check if decryption matches known plaintext
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

def demonstrate_brute_force(max_attempts: int):
    """
    Demonstrate a brute force attack on DES encryption.
    """
    print("Generating test case...")
    plaintext, original_key, ciphertext = generate_test_case()
    
    print(f"Plaintext: {plaintext}")
    print(f"Original Key: {original_key}")
    print(f"Ciphertext: {ciphertext}\n{bin2hex(ciphertext)}")
    
    print(f"\nStarting brute force attack with {max_attempts} attempts...")
    
    found_key = brute_force_attack(ciphertext, plaintext, max_attempts=max_attempts)
    
    if found_key:
        print(f"\nSuccess! Found key: {found_key}")
        print(f"Original key was: {original_key}")
    else:
        print("\nAttack failed to find the key within the attempt limit")

if __name__ == "__main__":
    max_attempts = 2**20
    demonstrate_brute_force(max_attempts = max_attempts) 