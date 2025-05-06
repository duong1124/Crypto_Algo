from algorithms import TripleDES

from utils import hex2bin, bin2hex, bin2dec, dec2bin, hex2dec, dec2hex

tdes = TripleDES()

plaintext = "123456ABCD132536" 
plaintext = hex2bin(plaintext)

k1 = 'AABB09182736CCDD'
# Randomly mutate the key from k1 using a seed value
k2 = tdes.mutate_key(k1, seed = 1)
k3 = tdes.mutate_key(k1, seed = 2) 

k1b = hex2bin(k1)
k2b = hex2bin(k2)
k3b = hex2bin(k3)

cipher = tdes.encrypt(plaintext, k1b, k2b, k3b)
print("Encrypted:", bin2hex(cipher))

decrypted = tdes.decrypt(cipher, k1b, k2b, k3b)
print("Decrypted:", bin2hex(decrypted))
