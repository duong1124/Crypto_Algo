# Cryptography Algorithms Implementation

This project aims for implementations of various cryptographic algorithms. The project focuses on providing clear, educational implementations of morden cryptographic methods.

## Features
### Utility Functions

The `utils` folder contains :
- General helper function at `helpers.py`. 
- Other specific helper functions for algo independently such as `des_helpers.py`.

#### Helper Functions (`helpers.py`):
- Binary/Hex/Decimal Conversions

- Cryptographic Operations:
  - `xor`
  - `circular_shift_left`
  - `split_half`
  - `swap_half`

- Data Handling
- Performance Evaluating

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Each algorithm module can be imported and used independently in folder `examples`:

```python
from src.algorithms.aes import AES
from src.algorithms.rsa import RSA

# Example usage
aes = AES()
encrypted = aes.encrypt("Hello, World!")
decrypted = aes.decrypt(encrypted)
```
### Caution
- To run the algorithms in `examples`, check for appropriate path and import.
- For example: Run DES algorithm at des_example in terminal by:
```terminal
python -m examples.des_example
```