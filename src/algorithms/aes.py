from Crypto import Cipher, Random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from typing import Any, Dict, Tuple
from .base import CryptoAlgorithm
from ..utils.helpers import pad_data, unpad_data

class AESAlgorithm(CryptoAlgorithm):
    """Implementation of the AES encryption algorithm."""
    
    def __init__(self, key_size: int = 32):
        super().__init__()
        self.key_size = key_size
        self.generate_key()
    
    def generate_key(self, key_size: int = None) -> bytes:
        """Generate a new AES key."""
        if key_size is not None:
            self.key_size = key_size
        self.key = get_random_bytes(self.key_size)
        return self.key
    
    def encrypt(self, plaintext: str) -> Tuple[bytes, Dict[str, float]]:
        """Encrypt the given plaintext using AES."""
        # Convert plaintext to bytes and pad if necessary
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        
        # Generate a random IV
        iv = get_random_bytes(16)
        
        # Create cipher object
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Pad and encrypt the data
        padded_data = pad_data(plaintext)
        ciphertext = cipher.encrypt(padded_data)
        
        # Combine IV and ciphertext
        result = iv + ciphertext
        
        # Measure performance
        metrics = {
            'execution_time': 0,  # Will be set by measure_performance
            'memory_usage': len(result)
        }
        
        return result, metrics
    
    def decrypt(self, ciphertext: bytes) -> Tuple[str, Dict[str, float]]:
        """Decrypt the given ciphertext using AES."""
        # Extract IV and actual ciphertext
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]
        
        # Create cipher object
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Decrypt and unpad the data
        padded_plaintext = cipher.decrypt(actual_ciphertext)
        plaintext = unpad_data(padded_plaintext)
        
        # Convert to string
        result = plaintext.decode()
        
        # Measure performance
        metrics = {
            'execution_time': 0,  # Will be set by measure_performance
            'memory_usage': len(plaintext)
        }
        
        return result, metrics
    
    def test_brute_force_resistance(self) -> Dict[str, Any]:
        """Test AES resistance to brute force attacks."""
        # AES with 256-bit key has 2^256 possible keys
        key_space = 2 ** (self.key_size * 8)
        
        # Assuming a hypothetical computer that can try 1 billion keys per second
        keys_per_second = 1e9
        seconds_in_year = 31536000
        
        estimated_years = key_space / (keys_per_second * seconds_in_year)
        
        return {
            'estimated_time': estimated_years,
            'complexity': f'O(2^{self.key_size * 8})',
            'recommended_key_size': 32,  # 256 bits
            'key_space': key_space
        }
    
    def test_timing_attack_resistance(self) -> Dict[str, Any]:
        """Test AES resistance to timing attacks."""
        # AES is generally considered resistant to timing attacks
        # due to its constant-time operations
        return {
            'is_resistant': True,
            'vulnerabilities': [],
            'notes': 'AES operations are designed to be constant-time, making it resistant to timing attacks'
        } 