from abc import ABC, abstractmethod
import time
from typing import Any, Dict, Tuple

class CryptoAlgorithm(ABC):
    """Base class for all cryptographic algorithms."""
    
    def __init__(self):
        self.key = None
        self.performance_metrics = {
            'encryption_time': 0,
            'decryption_time': 0,
            'memory_usage': 0
        }
    
    @abstractmethod
    def encrypt(self, plaintext: str) -> Tuple[Any, Dict[str, float]]:
        """Encrypt the given plaintext."""
        pass
    
    @abstractmethod
    def decrypt(self, ciphertext: Any) -> Tuple[str, Dict[str, float]]:
        """Decrypt the given ciphertext."""
        pass