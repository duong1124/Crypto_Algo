from algorithms import AES

input_bytes = bytearray(b"exampleplaintext") # 16 bytes
key = bytearray(b"thisisakey123456")         # 16 bytes
key_size = 16                                # Key size in bytes

aes = AES()

encrypted_data = AES.encrypt(input_bytes, key, key_size)
print("Encrypted:", encrypted_data)

decrypted_data = AES.decrypt(encrypted_data, key, key_size)
print("Decrypted:", decrypted_data)