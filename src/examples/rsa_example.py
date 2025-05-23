from algorithms import RSA

from utils import generate_prime_pair

plaintext = "hello"
p, q = generate_prime_pair(bit_size=32)
#p, q = 7, 13 # for testing
print(f"Generated primes: p = {p}, q = {q}")

rsa = RSA()
public_key, private_key = rsa.generate_keys(p, q)

print("------------------------ONE AT A TIME------------------------")
test_ciphertext = rsa.encrypt(plaintext, public_key, text=False, one_at_a_time=True)
print(f"Ciphertext: {test_ciphertext}")

test_decrypted = rsa.decrypt(test_ciphertext, private_key, text=False)
print(f"Decrypted: {test_decrypted}")

print("------------------------CONCAT------------------------")
true_ciphertext = rsa.encrypt(plaintext, public_key, text=False, one_at_a_time=False)
print(f"Ciphertext: {true_ciphertext}")

true_decrypted = rsa.decrypt(true_ciphertext, private_key, text=False)
print(f"Decrypted: {true_decrypted}")