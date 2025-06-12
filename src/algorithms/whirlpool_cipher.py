from utils.aes_helpers import AES_Helpers
from utils.aes_general_funcs import aes_64_Rcon, SIZE_64
from algorithms.base import CryptoAlgorithm

class WhirlpoolCipher(CryptoAlgorithm):
    def __init__(self):
        self.block_size = SIZE_64  # 64 bytes = 512 bits
        self.rounds = 10

    def encrypt(self, plaintext: bytearray, key: bytearray) -> bytearray:
        """Encrypt a 512-bit block with Whirlpool using the given 512-bit key."""

        helpers = AES_Helpers(self.block_size)
        state = plaintext[:]
        round_keys = self.key_expansion(key)

        # Pre-round transformation
        state = helpers.add_round_key(state, round_keys[0])

        # 10 rounds
        for round in range(1, self.rounds + 1):
            state = helpers.sub_bytes(state)
            state = helpers.shift_cols(state)
            state = helpers.mix_rows(state)
            state = helpers.add_round_key(state, round_keys[round])

        return state
    
    def key_expansion(self, key: bytearray) -> list:
        """
        Whirlpool key schedule: returns list of 11 round keys (K0...K10).
        Each round key is 64 bytes.
        RC_i: aes_64_Rcon[i-1] (i from 1 to 10)
        """
        helpers = AES_Helpers(self.block_size)
        round_keys = [key[:]]  # K0 = input cipherkey

        for round in range(1, self.rounds + 1):
            k = round_keys[-1][:]
            k = helpers.sub_bytes(k)
            k = helpers.shift_cols(k)
            k = helpers.mix_rows(k)

            rc = bytearray(aes_64_Rcon[round - 1])  # 8 bytes

            for i in range(8):
                k[i] ^= rc[i]
            round_keys.append(k)

        return round_keys
