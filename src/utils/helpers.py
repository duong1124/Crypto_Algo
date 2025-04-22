import os
import random
import string
from typing import Union, List, Dict
import numpy as np
import matplotlib.pyplot as plt

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
    """Convert a binary string to a hex string without 0x."""
    if bin_string.startswith('0b'):
        bin_string = bin_string[2:]
    return hex(int(bin_string, 2))[2:].upper()

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

def xor(a: str, b: str) -> str:
    """XOR two strings."""
    str = ""
    for i in range(len(a)):
        str += '1' if a[i] != b[i] else '0'
    return str

def circular_shift_left(key: str, shift: int) -> str:
    """Circular shift left the key.
    Args:
        key (str): The key to shift.
        shift (int): The number of shifts.
    Returns:
        str: The shifted key.
    """
    return key[shift:] + key[:shift]

def split_half(key: str) -> tuple[str, str]:
    """Split the key into two halves. 
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
    """Swap the two halves of the key.
    Args:
        left (str): The left half of the key.
        right (str): The right half of the key.
    Returns:
        tuple[str, str]: The swapped key.
    """
    return right, left

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