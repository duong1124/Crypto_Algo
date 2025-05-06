from utils.helpers import *
from algorithms.base import CryptoAlgorithm

class RSA(CryptoAlgorithm):
    def __init__(self):
        super().__init__()

    def generate_keys(self, p, q):
        """Generate RSA public and private keys based on two prime numbers.
        Args:
            p (int): First prime number.
            q (int): Second prime number.
        Returns:
            tuple: Public and private keys.
        """

        if not (sympy.isprime(p) and sympy.isprime(q)) or p == q:
            print("Both numbers must be prime and different.")
            return None, None

        n = p * q
        phi_n = (p - 1) * (q - 1)

        e = None
        for i in range(2, phi_n):
            if binary_gcd(i, phi_n) == 1:
                e = i
                break
        
        d = multiplicative_inverse(e, phi_n)

        public_key = (e, n)
        private_key = (d, n)

        return public_key, private_key

    def encrypt(self, msg, public_key, text = False):
        """Encrypt a message using the RSA algorithm.
        Args:
            msg (str): The message to encrypt.
            public_key (tuple): The public key (e, n).
            text (bool): If True, return the encrypted message as a string.
        Returns:
            str or list: The encrypted message as a string or a list of integers.
        """
        e, n = public_key
        encrypted = []
        for char in msg:
            pt = ord(char) - 96  # 'a' = 1, ..., 'z' = 26
            ct = advanceMod(pt, e, n)
            encrypted.append(ct + 96)  # Chuyển lại thành mã ASCII
        if text:
            encrypted = ''.join(map(lambda x: chr(x), encrypted))
        return encrypted

    def decrypt(self, cipher, private_key, text = False):
        """Decrypt a message using the RSA algorithm.
        Args:
            ciphertext (str or list): The ciphertext to decrypt.
            private_key (tuple): The private key (d, n).
            text (bool): If True, return the decrypted message as a string.
        Returns:
            str or list: The decrypted message as a string or a list of integers.
        """
        d, n = private_key
        decrypted = []
        if isinstance(cipher, str):
            cipher = [ord(char) for char in cipher]
            
        for ct in cipher:
            temp = ct - 96  # encrypted value, should be in range 1-26
            pt = advanceMod(temp, d, n)
            decrypted.append(pt + 96)  # Trả lại thành chữ cái
        if text:
            decrypted = ''.join(map(lambda x: chr(x), decrypted))
        return decrypted