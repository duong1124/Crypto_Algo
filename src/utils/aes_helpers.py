from .helpers import xor, dec2bin, hex2bin, bin2hex, bin2dec, hex2dec, dec2hex, circular_shift_left, split_half
from .aes_general_funcs import *

class AES_Helpers:
    def __init__(self, key_size: int):
        if key_size not in (SIZE_16, SIZE_24, SIZE_32, SIZE_64):
            raise ValueError("Invalid AES key size. Use 16, 24, 32 or 64 bytes.")
        self.key_size = key_size
        self.modified_512 = True if key_size == SIZE_64 else False
        
    def byte_to_state(self, block: bytearray) -> bytearray:
        """
        Convert 16/64-byte input into 4x4/8x8 AES column-major state.
        """
        n = 4 if not self.modified_512 else 8
        state = bytearray(n * n)
        for row in range(n):
            for col in range(n):
                if self.modified_512:
                    # Whirlpool: row-major
                    state[row * n + col] = block[row * n + col]
                else:
                    # AES: column-major
                    state[col * n + row] = block[row * n + col]
        return state

    def state_to_byte(self, state: bytearray) -> bytearray:
        """
        Convert AES column/row-major state back to 16/64-byte output.
        """
        n = 4 if not self.modified_512 else 8
        block = bytearray(n * n)
        for row in range(n):
            for col in range(n):
                if self.modified_512:
                    # Whirlpool: row-major
                    block[row * n + col] = state[row * n + col]
                else:
                    # AES: column-major
                    block[row * n + col] = state[col * n + row]
        return block

    def get_sbox_value(self, num):
        """Get a value from the S-Box"""
        return aes_sbox[num] if not self.modified_512 else aes_64_sbox[num]

    def get_rcon_value(self, num):
        """Get a value from the Rcon table"""
        return aes_Rcon[num]

    def core(self, word, iteration):
        """Key Schedule Core operation"""
        # rotate the 4-byte word 1 byte to the left
        word = circular_shift_left(word, 1)
        
        # apply S-Box substitution on all 4 parts of the 32-bit word
        for i in range(4):
            word[i] = self.get_sbox_value(word[i])
        
        # XOR the output of the rcon operation with iteration to the first part (leftmost) only
        word[0] = word[0] ^ self.get_rcon_value(iteration)
        
        return word

    def expand_key(self, key, key_size, expanded_key_size):
        """
        Expands an 128,192,256 key into an 176,208,240 bytes key
        Args:
            key (bytearray): The key to expand.
            key_size (int): The size of the key in bytes (16, 24, or 32).
            expanded_key_size (int): The size of the expanded key in bytes (176, 208, or 240).
        Returns:
            bytearray: The expanded key with expanded size.
        """
        expanded_key = bytearray(expanded_key_size)
        current_size = 0
        rcon_iteration = 1
        t = bytearray(4)  # temporary 4-byte variable
        
        # Set the 16, 24, 32 bytes of the expanded key to the input key
        for i in range(key_size):
            expanded_key[i] = key[i]
        current_size += key_size
        
        while current_size < expanded_key_size:
            # Assign the previous 4 bytes to the temporary value t
            for i in range(4):
                t[i] = expanded_key[(current_size - 4) + i]
            
            # Every 16, 24, 32 bytes we apply the core schedule to t and increment rcon_iteration
            if current_size % key_size == 0:
                t = self.core(t, rcon_iteration)
                rcon_iteration += 1
            
            # For 256-bit keys, we add an extra sbox to the calculation
            if key_size == SIZE_32 and ((current_size % key_size) == 16):
                for i in range(4):
                    t[i] = self.get_sbox_value(t[i])
            
            # We XOR t with the four-byte block key_size bytes before the new expanded key
            # This becomes the next four bytes in the expanded key
            for i in range(4):
                expanded_key[current_size] = expanded_key[current_size - key_size] ^ t[i]
                current_size += 1
                
        return expanded_key

    def sub_bytes(self, state):
        """
        Substitute all the values from the state with the value in the SBox
        using the state value as index for the SBox. For modified_512 (AES-512), use aes_64_sbox.
        """
        iteration = 16 if not self.modified_512 else 64 # not sure len(state) in bits or bytes

        for i in range(iteration):
            #state[i] = self.get_sbox_value(state[i])
            state[i] = aes_sbox[state[i]] if not self.modified_512 else aes_64_sbox[state[i]]
        return state

    @staticmethod
    def shift_row(state_row, nbr):
        """
        Shift a specific row to the left by nbr bytes.
        Args:
            state_row (bytearray): 4-byte row.
            nbr (int): The row number (0-based).
        """
        for i in range(nbr):
            tmp = state_row[nbr * 4]
            for j in range(3):
                state_row[nbr * 4 + j] = state_row[nbr * 4 + j + 1]
            state_row[nbr * 4 + 3] = tmp
        return state_row

    def shift_rows(self, state):
        """
        Iterate over the 4 rows and call shift_row() on each.
        Args:  
            state (bytearray): 4x4 AES column-major state.
        Returns:
            bytearray: The state after shifting rows. 
        """
        for i in range(4):
            state = self.shift_row(state, i)
        return state

    @staticmethod
    def shift_col(state, col_idx):
        """
        Shift a specific column (col_idx) of the 8x8 state down by col_idx bytes.
        Args:
            state (bytearray): 64 bytes, row-major.
            col_idx (int): The column number (0-based).
        Returns:
            bytearray: The state after shifting column col_idx.
        """
        n = 8
        # take col_idx
        col = [state[row * n + col_idx] for row in range(n)]
        # shift down col_idx positions
        shifted = [col[(row - col_idx) % n] for row in range(n)]
        
        for row in range(n):
            state[row * n + col_idx] = shifted[row]
        return state

    def shift_cols(self, state):
        """
        Iterate over the 8 columns and call shift_col() on each.
        Args:
            state (bytearray): 64 bytes, row-major.
        Returns:
            bytearray: The state after all columns have been shifted.
        """
        for col_idx in range(8):
            state = self.shift_col(state, col_idx)
        return state
    
    def add_round_key(self, state, round_key):
        """
        XOR the state with the round key.
        Args: 
            state (bytearray): 16-byte.
            round_key (bytearray): 16-byte.
        Returns:
            bytearray: The state after XOR with round key.
        """
        n = 16 if not self.modified_512 else 64
        for i in range(n):
            state[i] ^= round_key[i]
        return state

    @staticmethod
    def mix_column(column):
        """
        Mix a single column using the MixColumns matrix (C)
        Args:
            column (bytearray): 4-byte column
        Returns:
            bytearray: The mixed column
        """
        result = bytearray(4)
        for i in range(4):
            val = 0
            for j in range(4):
                val ^= galois_multiplication_GF8(column[j], MIX_COLUMNS_MATRIX[i][j])
            result[i] = val
        return result
    
    def mix_columns(self, state):
        """Iterate over the 4 columns and call mix_column() on each"""
        column = bytearray(4)
        
        # Iterate over the 4 columns
        for i in range(4):
            # Construct one column by iterating over the 4 rows
            for j in range(4):
                column[j] = state[j * 4 + i]
            
            # Apply the mix_column on one column
            column = self.mix_column(column)
            
            # Put the values back into the state
            for j in range(4):
                state[j * 4 + i] = column[j]
                
        return state

    @staticmethod
    def mix_row(row):
        """
        Mix a single row using the MixRows matrix
        Args:
            column (bytearray): 8-byte column
        Returns:
            bytearray: The mixed row
        """
        result = bytearray(8)
        for i in range(8):
            val = 0
            for j in range(8):
                val ^= galois_multiplication_GF8(row[j], MIX_ROWS_MATRIX[i][j], modulus=0x11D) # 0x11D for AES-512
            result[i] = val
        return result

    '''
    def mix_rows(self, state):
        row = bytearray(8)

        # Iterate over the 8 rows
        for i in range(8):
            # Construct one row by iterating over 8 cols
            for j in range(8):
                row[j] = state[j * 8 + i]

            # Then apply the mix_row on one row
            row = self.mix_row(row)

            # Put the value back into the state
            for j in range(8):
                state[j * 8 + i] = row[j]
        
        return state
    '''

    def mix_rows(self, state):
        new_state = bytearray(64)
        for row in range(8):
            row_bytes = state[row*8:(row+1)*8]
            mixed = self.mix_row(row_bytes)
            new_state[row*8:(row+1)*8] = mixed
        return new_state

    @staticmethod
    def create_round_key(expanded_key, round_key_pointer):
        """Create a round key from the expanded key"""
        round_key = bytearray(16)
        
        # Iterate over the columns
        for i in range(4):
            # Iterate over the rows
            for j in range(4):
                round_key[i + (j * 4)] = expanded_key[(round_key_pointer * 16) + (i * 4) + j]
        
        return round_key

    @staticmethod
    def inv_sub_bytes(state):
        """Apply the inverse SubBytes transformation"""
        for i in range(16):
            state[i] = aes_rsbox[state[i]]
        return state

    @staticmethod
    def inv_shift_row(state, nbr):
        """
        Each iteration shifts the row to the right by 1
        
        state is a 16-byte array representing 4x4 matrix
        nbr is the row number (0-based)
        """
        for i in range(nbr):
            tmp = state[nbr * 4 + 3]
            for j in range(3, 0, -1):
                state[nbr * 4 + j] = state[nbr * 4 + j - 1]
            state[nbr * 4] = tmp
        return state
    
    def inv_shift_rows(self, state):
        """Apply the inverse ShiftRows transformation"""
        for i in range(4):
            state = self.inv_shift_row(state, i)
        return state

    @staticmethod
    def inv_mix_column(column):
        """
        Mix a single column in the inverse direction using the InvMixColumns matrix (C^-1)
        Args:
            column (bytearray): 4-byte column
        Returns:
            bytearray: The mixed column
        """
        result = bytearray(4)
        for i in range(4):
            val = 0
            for j in range(4):
                val ^= galois_multiplication_GF8(column[j], INV_MIX_COLUMNS_MATRIX[i][j])
            result[i] = val
        return result
    
    def inv_mix_columns(self, state):
        """Apply the inverse MixColumns transformation"""
        column = bytearray(4)
        
        # Iterate over the 4 columns
        for i in range(4):
            # Construct one column by iterating over the 4 rows
            for j in range(4):
                column[j] = state[j * 4 + i]
            
            # Apply the inv_mix_column on one column
            column = self.inv_mix_column(column)
            
            # Put the values back into the state
            for j in range(4):
                state[j * 4 + i] = column[j]
                
        return state