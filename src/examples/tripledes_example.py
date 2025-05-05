from algorithms import TripleDES

from utils import hex2bin, bin2hex, bin2dec, dec2bin, hex2dec, dec2hex

tdes = TripleDES()

plaintext = "123456ABCD132536" 
plaintext = hex2bin(plaintext)

k1 = 'AABB09182736CCDD'
k2 = '2B77956B9B3E7E12'
k3 = '4A14508D5D44767A'

k1b = hex2bin(k1)
k2b = hex2bin(k2)
k3b = hex2bin(k3)

cipher = tdes.encrypt(plaintext, k1b, k2b, k3b)
print("Encrypted:", bin2hex(cipher))

decrypted = tdes.decrypt(cipher, k1b, k2b, k3b)
print("Decrypted:", bin2hex(decrypted))
