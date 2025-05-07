from algorithms import ECC_GFp, ECC_GF2n
from tests import ECCTester

def test_ecc():
    tester = ECCTester()
    tester.run_all_tests()

# Test ECC tests
ECC_test = ECCTester()
ECC_test.run_all_tests()

# ECC algorithms encryption and decryption

#plaintext = ""
#key?
ECC_p = ECC_GFp()
#ECC_p_ciphertext = ECC_p.encrypt()?
#decrypt?

ECC_2n = ECC_GF2n()
#ECC_2n_ciphertext = ECC_GF2n.encrypt()?
#decrypt?