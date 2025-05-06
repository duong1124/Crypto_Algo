from utils.aes_helpers import *
from utils.helpers import *
from algorithms.base import CryptoAlgorithm

class AES(CryptoAlgorithm):
    """Implementation of the AES encryption algorithm."""
    
    #def __init__(self, key_size: int = 128?):
    def __init__(self):
        super().__init__()

    def encrypt(input_bytes: bytearray, key: bytearray, key_size: int) -> bytearray:
        """Encrypt a 16-byte block with AES using the given key."""
        rounds = {16: 10, 24: 12, 32: 14}.get(key_size)
        if rounds is None:
            raise ValueError("Invalid AES key size. Use 16, 24, or 32 bytes.")
        
        expanded_key = expand_key(key, key_size, 16 * (rounds + 1))
        state = byte_to_state(input_bytes)

        # Initial Round
        state = add_round_key(state, create_round_key(expanded_key, 0))

        # Main Rounds
        for round_idx in range(1, rounds):
            state = sub_bytes(state)
            state = shift_rows(state)
            state = mix_columns(state)
            state = add_round_key(state, create_round_key(expanded_key, round_idx))

        # Final Round (no MixColumns)
        state = sub_bytes(state)
        state = shift_rows(state)
        state = add_round_key(state, create_round_key(expanded_key, rounds))

        return state_to_byte(state)

    def decrypt(input_bytes: bytearray, key: bytearray, key_size: int) -> bytearray:
        """Decrypt a 16-byte block with AES using the given key."""
        rounds = {16: 10, 24: 12, 32: 14}.get(key_size)
        if rounds is None:
            raise ValueError("Invalid AES key size. Use 16, 24, or 32 bytes.")
        
        expanded_key = expand_key(key, key_size, 16 * (rounds + 1))
        state = byte_to_state(input_bytes)

        # Initial Round
        state = add_round_key(state, create_round_key(expanded_key, rounds))

        # Main Rounds
        for round_idx in range(rounds - 1, 0, -1):
            state = inv_shift_rows(state)
            state = inv_sub_bytes(state)
            state = add_round_key(state, create_round_key(expanded_key, round_idx))
            state = inv_mix_columns(state)

        # Final Round (no InvMixColumns)
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, create_round_key(expanded_key, 0))

        return state_to_byte(state)
