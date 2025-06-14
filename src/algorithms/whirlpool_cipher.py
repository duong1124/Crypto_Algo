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
        state = bytearray(plaintext)
        round_keys = self.key_expansion(key)

        # Pre-round transformation
        state = helpers.add_round_key(state, bytearray(round_keys[0]))

        # 10 rounds
        for round in range(1, self.rounds + 1):
            state = helpers.sub_bytes(state)
            state = helpers.shift_cols(state)
            state = helpers.mix_rows(state)
            state = helpers.add_round_key(state, round_keys[round])

        return state
    
    def decrypt(self):
        pass

    def key_expansion(self, key: bytearray) -> list:
        helpers = AES_Helpers(self.block_size)
        round_keys = [key[:]]  # K0 = input cipherkey

        for round in range(1, self.rounds + 1):
            k = round_keys[-1][:]
            k = helpers.sub_bytes(k)
            k = helpers.shift_cols(k)
            k = helpers.mix_rows(k)

            rc = bytearray(64)
            rc[0:8] = aes_64_Rcon[round - 1] 

            # K[i] = K[i-1] ⊕ RC[i] ⊕ γ(K[i-1])
            k = bytearray([k[j] ^ rc[j] for j in range(64)])
            round_keys.append(k)

        return round_keys
