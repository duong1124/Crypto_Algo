from .base import CryptoAlgorithm
from utils.ecc_helpers import *
from typing import Any, Dict, Tuple
import time

# ECC over GF(p)
class ECC_GFp(CryptoAlgorithm):
    def __init__(self):
        super().__init__()
        self.curve = None
        self.G = None
        self.n = None
        self.key = None       # Private key
        self.public_key = None # Our public key
        self.recipient_public_key = None # Recipient's public key for encryption
    
    def set_curve(self, a: int, b: int, p: int, G: Tuple[int, int], n: int):
        self.curve = EllipticCurveGFp(a, b, p)
        self.G = G
        self.n = n
    
    def generate_keypair(self) -> Tuple[int, Tuple[int, int]]:
        """
        Generate a private-public key pair for ECDH over GF(p).
        """
        if not self.curve or not self.G or not self.n:
            raise ValueError("Curve parameters must be set before generating keypair")
        while True:
            # Generate a random private key between 1 and n-1
            private_key = random.randint(1, self.n - 1)
            # Calculate the public key as Q = private_key * G
            public_key = self.curve.multiply_point(self.G, private_key)
            # Ensure the public key is not the point at infinity
            if public_key is not None:
                self.key = private_key  # Store private key
                self.public_key = public_key  # Store our public key
                return private_key, public_key
            
    def compute_shared_secret(self, private_key: int, other_public_key: Tuple[int, int]) -> int:
        """
        Compute the shared secret for ECDH.
        
        Args:
            private_key: Your private key
            other_public_key: The other party's public key
        
        Returns:
            shared_secret: A point on the curve that serves as the shared secret
        """
        
        if not self.curve:
            raise ValueError("Curve must be set before computing shared secret")
        # Validate the public key
        if other_public_key is None:
            raise ValueError("Invalid public key: Point at infinity")
        # Calculate the shared secret as private_key * other_public_key
        shared_secret = self.curve.multiply_point(other_public_key, private_key)
        # Check if the result is the point at infinity
        if shared_secret is None:
            print("Warning: Shared secret is point at infinity, using alternative value")
            return 1
        
        # For GF(2^n) curves, we need to handle the shared secret differently
        if isinstance(self, EllipticCurveGF2n):
            # Use both x and y coordinates to derive the shared secret
            x, y = shared_secret
            # Combine them in a deterministic way
            combined = (x << self.degree) | y
            return combined
        
        return shared_secret[0]
    
    def set_recipient_key(self, recipient_public_key: Tuple[int, int]):
        """
        Set the recipient's public key for encryption.
        """
        if not isinstance(recipient_public_key, tuple) or len(recipient_public_key) != 2:
            raise TypeError(f"Expected recipient_public_key to be a tuple (x,y), got {type(recipient_public_key)}")
        self.recipient_public_key = recipient_public_key
    
    def encrypt(self, plaintext: str) -> Tuple[Tuple[Tuple[int, int], int], Dict[str, float]]:
        """
        Encrypt a message using the ECIES-like scheme for GF(p).
        """
        if not self.curve or not self.G or not self.n:
            raise ValueError("Curve parameters must be set before encryption")
        
        if not self.recipient_public_key:
            raise ValueError("Recipient's public key must be set before encryption")
        
        start_time = time.time()
        message = int(hashlib.sha256(plaintext.encode()).hexdigest(), 16) % self.curve.p
        max_attempts = 10
        for _ in range(max_attempts):
            # Generate a random ephemeral key pair
            k = random.randint(1, self.n - 1)
            R = self.curve.multiply_point(self.G, k)
            
            # Compute the shared secret using recipient's public key
            S = self.curve.multiply_point(self.recipient_public_key, k)
            
            # Check if shared secret is valid
            if S is not None:
                shared_secret = S[0]
                # Simple encryption: C2 = message XOR shared_secret
                C2 = message ^ shared_secret
                self.performance_metrics['encryption_time'] = time.time() - start_time
                return (R, C2), self.performance_metrics
        raise ValueError("Encryption failed: Could not compute valid shared secret")
    
    def decrypt(self, ciphertext: Tuple[Tuple[int, int], int]) -> Tuple[str, Dict[str, float]]:
        """
        Decrypt a message using the ECIES-like scheme for GF(p).
        """
        if not self.curve or not self.key:
            raise ValueError("Curve and private key must be set before decryption")
        start_time = time.time()
        R, C2 = ciphertext
        
        # Compute the shared secret using our private key
        S = self.curve.multiply_point(R, self.key)
        if S is None:
            raise ValueError("Decryption failed: Invalid shared secret")
        
        shared_secret = S[0]
        # Simple decryption: message = C2 XOR shared_secret
        message = C2 ^ shared_secret
        self.performance_metrics['decryption_time'] = time.time() - start_time
        return str(message), self.performance_metrics
# ECC over GF(2^n)
class ECC_GF2n(CryptoAlgorithm):
    # ECC over GF(2^n) class ECC_GF2n(CryptoAlgorithm):
    def __init__(self):
        super().__init__()
        self.curve = None
        self.G = None
        self.n = None
        self.key = None           # Private key
        self.public_key = None    # Our public key
        self.recipient_public_key = None  # Recipient's public key for encryption

    def set_curve(self, a: int, b: int, irreducible_poly: int, degree: int, G: Tuple[int, int], n: int):
        self.curve = EllipticCurveGF2n(a, b, irreducible_poly, degree)
        self.G = G
        self.n = n

    def generate_keypair(self) -> Tuple[int, Tuple[int, int]]:
        """
        Generate a private-public key pair for ECDH over GF(2^n).
        
        Returns:
            (private_key, public_key): The generated key pair
        """
        if not self.curve or not self.G or not self.n:
            raise ValueError("Curve parameters must be set before generating keypair")
        
        while True:
            # Generate a random private key between 1 and n-1
            private_key = random.randint(1, self.n - 1)
            
            # Calculate the public key as Q = private_key * G
            public_key = self.curve.multiply_point(self.G, private_key)
            
            # Ensure the public key is not the point at infinity
            if public_key is not None:
                self.key = private_key       # Store private key
                self.public_key = public_key  # Store our public key
                return private_key, public_key

    def compute_shared_secret(self, private_key: int, other_public_key: Tuple[int, int]) -> int:
        """
        Compute the shared secret for ECDH.
        
        Args:
            private_key: Your private key
            other_public_key: The other party's public key
            
        Returns:
            shared_secret: A value derived from a point on the curve that serves as the shared secret
        """
        if not self.curve:
            raise ValueError("Curve must be set before computing shared secret")
            
        # Validate the public key
        if other_public_key is None:
            raise ValueError("Invalid public key: Point at infinity")
            
        # Calculate the shared secret as private_key * other_public_key
        shared_secret = self.curve.multiply_point(other_public_key, private_key)
            
        # Check if the result is the point at infinity
        if shared_secret is None:
            print("Warning: Shared secret is point at infinity, using alternative value")
            return 1
            
        # For GF(2^n) curves, we use both x and y coordinates to derive the shared secret
        x, y = shared_secret
        # Combine them in a deterministic way
        combined = (x << self.curve.degree) | y
        return combined

    def set_recipient_key(self, recipient_public_key: Tuple[int, int]):
        """
        Set the recipient's public key for encryption.
        """
        if not isinstance(recipient_public_key, tuple) or len(recipient_public_key) != 2:
            raise TypeError(f"Expected recipient_public_key to be a tuple (x,y), got {type(recipient_public_key)}")
        self.recipient_public_key = recipient_public_key

    def encrypt(self, plaintext: str) -> Tuple[Tuple[Tuple[int, int], int], Dict[str, float]]:
        """
        Encrypt a message using the ECIES-like scheme for GF(2^n).
        
        Returns:
            ((R, C2), performance_metrics): The encrypted ciphertext and performance metrics
        """
        if not self.curve or not self.G or not self.n:
            raise ValueError("Curve parameters must be set before encryption")
            
        if not self.recipient_public_key:
            raise ValueError("Recipient's public key must be set before encryption")
            
        start_time = time.time()
        message = int(hashlib.sha256(plaintext.encode()).hexdigest(), 16) % (2**self.curve.degree)
        
        max_attempts = 10
        for _ in range(max_attempts):
            # Generate a random ephemeral key pair
            k = random.randint(1, self.n - 1)
            R = self.curve.multiply_point(self.G, k)
            
            # Compute the shared secret using recipient's public key
            S = self.curve.multiply_point(self.recipient_public_key, k)
            
            # Check if shared secret is valid
            if S is not None:
                x, y = S
                shared_secret = (x << self.curve.degree) | y
                
                # Simple encryption: C2 = message XOR shared_secret
                C2 = message ^ shared_secret
                
                self.performance_metrics['encryption_time'] = time.time() - start_time
                return (R, C2), self.performance_metrics
                
        raise ValueError("Encryption failed: Could not compute valid shared secret")

    def decrypt(self, ciphertext: Tuple[Tuple[int, int], int]) -> Tuple[str, Dict[str, float]]:
        """
        Decrypt a message using the ECIES-like scheme for GF(2^n).
        
        Args:
            ciphertext: The encrypted ciphertext (R, C2)
            
        Returns:
            (decrypted_message, performance_metrics): The decrypted message and performance metrics
        """
        if not self.curve or not self.key:
            raise ValueError("Curve and private key must be set before decryption")
            
        start_time = time.time()
        R, C2 = ciphertext
        
        # Compute the shared secret using our private key
        S = self.curve.multiply_point(R, self.key)
        
        if S is None:
            raise ValueError("Decryption failed: Invalid shared secret")
            
        x, y = S
        shared_secret = (x << self.curve.degree) | y
        
        # Simple decryption: message = C2 XOR shared_secret
        message = C2 ^ shared_secret
        
        self.performance_metrics['decryption_time'] = time.time() - start_time
        return str(message), self.performance_metrics