from utils.helpers import *
from algorithms.base import CryptoAlgorithm
from typing import List

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
            print("Both numbers must be seperated primes.")
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

    def encrypt(self, msg, public_key, text = False, one_at_a_time = True):
        """Encrypt a message using the RSA algorithm.
        Args:
            msg (str): The message to encrypt.
            public_key (tuple): The public key (e, n).
            text (bool): If True, return the encrypted message as a string.
            one_at_a_time (bool): If True, encrypt one character at a time.
        Returns:
            int or list: list of int if one_at_a_time, else int.
        """
        e, n = public_key

        pt = text_to_z26(msg, one_at_a_time=one_at_a_time)

        if isinstance(pt, List):
            encrypted = [advanceMod_SM(num, e, n) for num in pt]
        elif isinstance(pt, int):
            encrypted = advanceMod_SM(pt, e, n)
        else:
            raise ValueError("Invalid plaintext format. Expected int or list of int.")
        
        return encrypted
    
    def decrypt(self, cipher, private_key, text = False):
        """Decrypt a message using the RSA algorithm.
        Args:
            ciphertext (int or list): The ciphertext to decrypt.
            private_key (tuple): The private key (d, n).
            text (bool): If True, return the decrypted message as a string.
            one_at_a_time (bool): If True, decrypt one character at a time. If False,
        Returns:
            str or list: The decrypted message as a string or a list of integers.
        """
        d, n = private_key
        decrypted = []

        if isinstance(cipher, list):
            decrypted = []
            for ct in cipher:
                pt = advanceMod_SM(ct, d, n)
                decrypted.append(pt)
            if text:
                decrypted = ''.join(map(lambda x: z26_to_char(x), decrypted))

        elif isinstance(cipher, int):
            pt_int = advanceMod_SM(cipher, d, n)
            pt_numerical_str = str(pt_int)

            if len(pt_numerical_str) % 2 != 0:
                pt_numerical_str = pt_numerical_str.zfill(len(pt_numerical_str) + 1) # pad with 0

            for i in range(0, len(pt_numerical_str), 2):
                temp = int(''.join([pt_numerical_str[i], pt_numerical_str[i+1]]))
                decrypted.append(temp)
            
            decrypted = ''.join(map(lambda x: z26_to_char(x), decrypted))
        
        else:
            raise ValueError("Invalid ciphertext format. Expected int or list of int.")

        return decrypted