from utils.aes_helpers import AES_Helpers
from utils.aes_general_funcs import *
from utils.helpers import *
from algorithms.base import CryptoAlgorithm

class AES(CryptoAlgorithm):
    """Implementation of the AES encryption algorithm."""
    
    #def __init__(self, key_size: int = 128?):
    def __init__(self, key_size: int = 16):
        super().__init__()
        self.key_size = key_size
        
    def encrypt(self, input_bytes: bytearray, key: bytearray) -> bytearray:
        """Encrypt a 16-byte block with AES using the given key."""
        rounds = {16: 10, 24: 12, 32: 14, 64: 10}.get(self.key_size)
        if rounds is None:
            raise ValueError("Invalid AES key size. Use 16, 24, 32 or 64 bytes.")
        helpers = AES_Helpers(self.key_size)

        expanded_key = helpers.expand_key(key, self.key_size, 16 * (rounds + 1))
        state = helpers.byte_to_state(input_bytes)

        # Initial round key addition
        state = helpers.add_round_key(state, helpers.create_round_key(expanded_key, 0))

        for round_idx in range(1, rounds):
            state = helpers.sub_bytes(state)
            state = helpers.shift_rows(state)
            state = helpers.mix_columns(state)
            state = helpers.add_round_key(state, helpers.create_round_key(expanded_key, round_idx))

        # Final round (no MixColumns)
        state = helpers.sub_bytes(state)
        state = helpers.shift_rows(state)
        state = helpers.add_round_key(state, helpers.create_round_key(expanded_key, rounds))
        
        return helpers.state_to_byte(state)

    def decrypt(self, input_bytes: bytearray, key: bytearray) -> bytearray:
        """Decrypt a 16-byte block with AES using the given key."""
        rounds = {16: 10, 24: 12, 32: 14, 64: 10}.get(self.key_size)
        if rounds is None:
            raise ValueError("Invalid AES key size. Use 16, 24, 32 or 64 bytes.")
        helpers = AES_Helpers(self.key_size)
        
        expanded_key = helpers.expand_key(key, self.key_size, 16 * (rounds + 1))
        state = helpers.byte_to_state(input_bytes)

        # Initial round key addition
        state = helpers.add_round_key(state, helpers.create_round_key(expanded_key, rounds))
        
        for round_idx in range(rounds - 1, 0, -1):
            state = helpers.inv_shift_rows(state)
            state = helpers.inv_sub_bytes(state)
            state = helpers.add_round_key(state, helpers.create_round_key(expanded_key, round_idx))
            state = helpers.inv_mix_columns(state)
        
        # Final round (no InvMixColumns)
        state = helpers.inv_shift_rows(state)
        state = helpers.inv_sub_bytes(state)
        state = helpers.add_round_key(state, helpers.create_round_key(expanded_key, 0))

        return helpers.state_to_byte(state)
