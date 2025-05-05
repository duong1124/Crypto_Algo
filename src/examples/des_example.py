from algorithms import DES

from utils import hex2bin, bin2hex, bin2dec, dec2bin, hex2dec, dec2hex, split_half, circular_shift_left

plaintext = "123456ABCD132536"
plaintext = hex2bin(plaintext)

key = "AABB09182736CCDD"
print(f"Key size: {len(key)}")
keyb = hex2bin(key)

des = DES()
ciphertext = des.encrypt(plaintext, keyb, print_round_text=True)
print(f"Ciphertext: {bin2hex(ciphertext)}")
decrypted_text = des.decrypt(ciphertext, keyb, print_round_text=True)
print(f"Decrypted text: {bin2hex(decrypted_text)}")