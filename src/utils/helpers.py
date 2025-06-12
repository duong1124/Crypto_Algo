import os
import random
import string
import math
import sympy
from typing import Union, List, Dict
import numpy as np
import matplotlib.pyplot as plt
MAX_64BIT = 0xffffffffffffffff

def hex2bin(hex_string: str) -> str:
    """Convert a hex string to a binary string without 0b."""
    # return bin(int(hex_string, 16))[2:]
    if hex_string.startswith('0x'):
        hex_string = hex_string[2:]

    hex_string = hex_string.upper()

    mp = {'0': "0000",
		'1': "0001",
		'2': "0010",
		'3': "0011",
		'4': "0100",
		'5': "0101",
		'6': "0110",
		'7': "0111",
		'8': "1000",
		'9': "1001",
		'A': "1010",
		'B': "1011",
		'C': "1100",
		'D': "1101",
		'E': "1110",
		'F': "1111"}

    bin = ""

    for i in range(len(hex_string)):
        bin = bin + mp[hex_string[i]]

    return bin
        
def bin2hex(bin_string: str) -> str:
    """
    Convert a binary string to a hex string without 0x and with zero fill.
    Args:
        bin_string (str): The binary string to convert.
    Returns:
        str: The hex string.
    """
    if bin_string.startswith('0b'):
        bin_string = bin_string[2:]
    res = hex(int(bin_string, 2))[2:].upper()
    res = res.zfill(len(bin_string) // 4)
    return res

def bin2dec(bin_string: str) -> int:
    """Convert a binary string to a decimal integer."""
    if bin_string.startswith('0b'):
        bin_string = bin_string[2:]
    return int(bin_string, 2)

def dec2bin(dec_int: int, size: int = None) -> str:
    """Convert a decimal integer to a binary string with fixed length."""
    if isinstance(dec_int, str):
        dec_int = int(dec_int, 10)
    bin_str = bin(dec_int)[2:]  # remove '0b'
    if size is not None:
        return bin_str.zfill(size)
    return bin_str

def hex2dec(hex_string: str) -> int:
    """Convert a hex string to a decimal integer."""
    if hex_string.startswith('0x'):
        hex_string = hex_string[2:]
    return int(hex_string, 16)

def dec2hex(dec_int: int) -> str:
    """Convert a decimal integer to a hex string without 0x."""
    return hex(dec_int)[2:].upper()

def text_to_binary(text: str) -> str:
    """Convert a text string to a binary string."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary: str) -> str:
    """Convert a binary string to a text string."""
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def xor(a: str, b: str) -> str:
    """XOR two strings."""
    str = ""
    for i in range(len(a)):
        str += '1' if a[i] != b[i] else '0'
    return str

def circular_shift_left(key: str, shift: int) -> str:
    """
    Circular shift left the key.
    Args:
        key (str): The key to shift.
        shift (int): The number of shifts.
    Returns:
        str: The shifted key.
    """
    return key[shift:] + key[:shift]

def split_half(key: str) -> tuple[str, str]:
    """
    Split the key into two halves. 
    Args:
        key (str): The key to split.
    Returns:
        tuple[str, str]: The left and right halves of the key.
    """
    half = len(key) // 2
    left = key[:half]
    right = key[half:]
    return left, right

def swap_half(left: str, right: str) -> tuple[str, str]:
    """
    Swap the two halves of the key.
    Args:
        left (str): The left half of the key.
        right (str): The right half of the key.
    Returns:
        tuple[str, str]: The swapped key.
    """
    return right, left

def rotate_right(n, r):
    return ((n >> r) | (n << (64 - r))) & MAX_64BIT

def shift_left(n, r):
    return n << r

def is_prime(n):
    """
    Check if a number is prime.
    Args:
        n (int): 
    Returns:
        bool: True if prime, False otherwise.
    """
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def binary_gcd(a, b):
    """
    GCD(a, b) using binary GCD algorithm.
    Args:
        a (int): First number.
        b (int): Second number.
    Returns:
        int: GCD of a and b.
    """
    if (a == 0):
        return b

    if (b == 0):
        return a

    # K is the greatest power of 2 that divides both a and b.
    k = 0

    while(((a | b) & 1) == 0):
        a = a >> 1
        b = b >> 1
        k = k + 1

    # Dividing a by 2 until a becomes odd
    while ((a & 1) == 0):
        a = a >> 1

    while(b != 0):

        # If b is even, remove all
        # factor of 2 in b
        while ((b & 1) == 0):
            b = b >> 1

        # Now a and b are both odd. Swap if
        # necessary so a <= b, then set
        # b = b - a (which is even).
        if (a > b):
          a, b = b, a
        b = (b - a)

    # restore common factors of 2
    return (a << k)

def gcd(a, b):
    """GCD(a, b) using Euclid algorithm.
    Args:
        a (int): First.
        b (int): Second.
    Returns:
        int: GCD(a, b).
    """
    while b != 0:
        a, b = b, a % b
    return a

def advanceMod(a, b, c):
    '''
    Calculate a^b mod c using modular exponentiation (LSB to MSB).
    Args:
        a (int): The base.
        b (int): The exponent.
        c (int): The modulus.
    Returns:
        int: a^b mod c.
    '''
    result = 1

    a = a % c
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % c
        b //= 2
        a = (a * a) % c

    return result

def advanceMod_SM(a, b, c):
    '''
    Calculate a^b mod c using square-and-multiply algorithm in class (MSB to LSB).
    Args:
        a (int): The base.
        b (int): The exponent.
        c (int): The modulus.
    Returns:
        int: a^b mod c.
    '''
    bits = bin(b)[2:]
    result = 1

    for bit in bits:
        result = (result * result) % c
        if bit == '1':
            result = (result * a) % c

    return result

def multiplicative_inverse(e, t):
    '''
    Calculate mul_inv of e modulo t using the Extended Euclidean Algorithm.
    Args:
        e (int): The number to find the inverse of.
        t (int): The modulus.
    Returns:
        int: The mul_inverse of e mod t. None if not exists.
    '''
    # Extended Euclidean Algorithm
    t0, t1 = 0, 1
    r0, r1 = t, e
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        t0, t1 = t1, t0 - q * t1
    if r0 > 1:
        return None  # No inverse
    return t0 % t


def generate_prime_pair(bit_size = 32):
    """Generate two different prime numbers of specified bit size
    Args:
        bit_size (int): The bit size of the primes to generate, default = 32.
    Returns:
        tuple: (p, q) - Two different prime numbers
    """
    # Generate first prime
    p = sympy.randprime(2**(bit_size-1), 2**bit_size)
    
    # Generate second prime (ensure it's different from p)
    q = sympy.randprime(2**(bit_size-1), 2**bit_size)
    while p == q:
        q = sympy.randprime(2**(bit_size-1), 2**bit_size)
    
    return p, q
    
def miller_rabin_prime(bit_size, k=40):
    """Generate a prime number of specified bit size using Miller-Rabin test
    
    Args:
    bit_size (int): The bit size of the prime to generate
    k (int): Number of iterations for Miller-Rabin test
    
    Returns:
    int: A probable prime number
    """
    def is_probably_prime(n, k=40):
        """Miller-Rabin primality test"""
        if n == 2 or n == 3:
            return True
        if n <= 1 or n % 2 == 0:
            return False
            
        # Write n as 2^r·d + 1
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
            
        # Witness loop
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
        
    # Generate a random odd number of the specified bit size
    while True:
        # Generate a random number with the top bit set (to ensure bit_size bits)
        # and bottom bit set (to ensure odd number)
        p = (1 << (bit_size - 1)) | random.getrandbits(bit_size - 2) | 1
        if is_probably_prime(p, k):
            return p

def z26_to_char(num: int) -> str:
    """Convert a number in Z_26 group (0 - 25) to its corresponding character.
    Args:
        num (int)
    Returns:
        str
    """
    if 0 <= num < 26:
        return chr(num + 97)  # 'a' is ASCII 97
    else:
        raise ValueError("Number must be in the range [0, 25]")

def text_to_z26(text: str, one_at_a_time: bool = True):
    """Convert text to Z_26 group representation (0 - 25).
    Args:
        text (str): The text to convert.
        one_at_a_time (bool): If True, convert one character at a time and return a list. Else, return a single integer after concat.
    Returns:
        int or list: The Z_26 representation of the text.
    """
    if one_at_a_time:
        return [ord(char) - 97 for char in text] 
    else:
        num_str = ''.join([f"{ord(char) - 97:02d}" for char in text.lower()]) # zeropad each converted char to 2 digits
        return int(num_str)

def whirlpool_pad(message: bytes) -> bytes:
    """
    Pad message for Whirlpool hash:
      Append a single '1' bit, then '0' bits to make length ≡ 256 mod 512,
      then append 256-bit (32 bytes) length field.
    """
    ml = len(message) * 8  # message length in bits
    # Append '1' bit (0x80), then as many '0' bits as needed
    pad = b'\x80'
    pad_len = (512 - ((ml + 8 + 256) % 512)) % 512  # bits to next 256 mod 512, minus 8 bits for 0x80
    pad += b'\x00' * ((pad_len // 8))
    # Append 256-bit length (32 bytes, big-endian)
    length_field = ml.to_bytes(32, byteorder='big')
    return message + pad + length_field

def generate_random_string(length: int = 16) -> str:
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def pad_data(data: Union[str, bytes], block_size: int = 16) -> bytes:
    """Pad data to match block size requirements."""
    if isinstance(data, str):
        data = data.encode()
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad_data(data: bytes) -> bytes:
    """Remove padding from data."""
    padding_length = data[-1]
    return data[:-padding_length]

def plot_performance_metrics(metrics: List[Dict[str, float]], algorithm_names: List[str]):
    """Plot performance metrics for different algorithms."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot encryption/decryption times
    enc_times = [m['encryption_time'] for m in metrics]
    dec_times = [m['decryption_time'] for m in metrics]
    
    x = np.arange(len(algorithm_names))
    width = 0.35
    
    ax1.bar(x - width/2, enc_times, width, label='Encryption')
    ax1.bar(x + width/2, dec_times, width, label='Decryption')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Encryption/Decryption Performance')
    ax1.set_xticks(x)
    ax1.set_xticklabels(algorithm_names)
    ax1.legend()
    
    # Plot throughput
    throughput = [m['throughput'] for m in metrics]
    ax2.bar(algorithm_names, throughput)
    ax2.set_ylabel('Throughput (bytes/second)')
    ax2.set_title('Algorithm Throughput')
    
    plt.tight_layout()
    plt.show()

def save_metrics_to_file(metrics: Dict[str, float], filename: str):
    """Save performance metrics to a file."""
    with open(filename, 'w') as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")

def load_metrics_from_file(filename: str) -> Dict[str, float]:
    """Load performance metrics from a file."""
    metrics = {}
    with open(filename, 'r') as f:
        for line in f:
            key, value = line.strip().split(': ')
            metrics[key] = float(value)
    return metrics 