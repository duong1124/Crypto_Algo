from algorithms import RSA

from utils import generate_prime_pair

plaintext = "hello"
p, q = generate_prime_pair(32)
#p, q = 7, 13 # for testing
print(f"Generated primes: p = {p}, q = {q}")

rsa = RSA()
public_key, private_key = rsa.generate_keys(p, q)

ciphertext = rsa.encrypt(plaintext, public_key, text=False)
print(f"Ciphertext: {ciphertext}")

decrypted_text = rsa.decrypt(ciphertext, private_key, text=True)
print(f"Decrypted text: {decrypted_text}")