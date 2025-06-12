"""
Utility functions for the cryptography project.
""" 
# conversion functions
from .helpers import hex2bin, bin2hex, bin2dec, dec2bin, hex2dec, dec2hex, text_to_binary, binary_to_text, text_to_z26, z26_to_char

# split and shift functions
from .helpers import split_half, circular_shift_left

# math functions
from .helpers import xor, gcd,  binary_gcd, is_prime, extended_gcd, multiplicative_inverse, advanceMod, advanceMod_SM

# prime generation functions
from .helpers import generate_prime_pair, miller_rabin_prime

from .metric_plot import plot_performance_metrics, save_metrics_to_file, load_metrics_from_file

from .helpers import whirlpool_pad
from .des_helpers import *
from .sha512_helpers import *
