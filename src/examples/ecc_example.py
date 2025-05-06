import hashlib
import sys
import os
# Add the parent directory of 'src' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.ecc import ECC_GFp, ECC_GF2n
from utils.ecc_helpers import EllipticCurveGFp, EllipticCurveGF2n

# Testing Class
class ECCTester:
    def __init__(self):
        self.ecc_gfp = ECC_GFp()
        self.ecc_gf2n = ECC_GF2n()
    
    def test_gfp(self):
        print("\n===== Testing GF(p) Implementation =====")
        p = 23
        a = 1
        b = 1
        curve = EllipticCurveGFp(a, b, p)
        points = []
        print(f"Points on the curve y^2 = x^3 + {a}x + {b} mod {p}:")
        for x in range(p):
            right = (x**3 + a*x + b) % p
            for y in range(p):
                if (y**2) % p == right:
                    point = (x, y)
                    points.append(point)
                    print(f"({x}, {y})", end=" ")
        print("\n")
        if not points:
            print("No points found on the curve!")
            return
        G = points[0]
        print(f"Base point G = {G}")
        n = len(points) + 1
        print(f"Using n = {n} (number of points + 1)")
        self.ecc_gfp.set_curve(a, b, p, G, n)
        P = points[1] if len(points) > 1 else G
        Q = points[2] if len(points) > 2 else G
        print(f"P = {P}, Q = {Q}")
        P_plus_Q = curve.add_points(P, Q)
        print(f"P + Q = {P_plus_Q}")
        P_doubled = curve.add_points(P, P)
        print(f"2P = {P_doubled}")
        k = 3
        kP = curve.multiply_point(P, k)
        print(f"{k}P = {kP}")
        
        print("\nTesting ECDH key exchange...")
        alice_private, alice_public = self.ecc_gfp.generate_keypair()
        print(f"Alice's private key: {alice_private}")
        print(f"Alice's public key: {alice_public}")
        bob_private, bob_public = self.ecc_gfp.generate_keypair()
        print(f"Bob's private key: {bob_private}")
        print(f"Bob's public key: {bob_public}")
        alice_shared = self.ecc_gfp.compute_shared_secret(alice_private, bob_public)
        bob_shared = self.ecc_gfp.compute_shared_secret(bob_private, alice_public)
        print(f"Alice's computed shared secret: {alice_shared}")
        print(f"Bob's computed shared secret: {bob_shared}")
        print(f"Shared secrets match: {alice_shared == bob_shared}")
        
        print("\nTesting encryption/decryption...")
        message = "Hello, ECC!"
        print(f"Original message: {message}")
        
        # Set the recipient key before encryption
        self.ecc_gfp.set_recipient_key(bob_public)
        
        # Using Alice's private key for encryption
        self.ecc_gfp.key = alice_private
        
        ciphertext, metrics = self.ecc_gfp.encrypt(message)
        print(f"Ciphertext: {ciphertext}")
        print(f"Encryption metrics: {metrics}")
        
        # Set Bob's private key for decryption
        self.ecc_gfp.key = bob_private
        
        decrypted, metrics = self.ecc_gfp.decrypt(ciphertext)
        print(f"Decrypted message: {decrypted}")
        print(f"Decryption metrics: {metrics}")
        
        # Verify the decryption was successful
        message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16) % p
        print(f"Original message hash: {message_hash}")
        print(f"Decryption successful: {str(message_hash) == decrypted}")
    
    def test_gf2n(self):
        print("\n===== Testing GF(2^n) Implementation =====")
        n = 4
        irreducible_poly = 0b10011
        a = 0b0001
        b = 0b0001
        curve = EllipticCurveGF2n(a, b, irreducible_poly, n)
        points = []
        print(f"Points on the curve y^2 + xy = x^3 + {bin(a)[2:]}x^2 + {bin(b)[2:]} in GF(2^{n}):")
        for x_val in range(1 << n):
            for y_val in range(1 << n):
                point = (x_val, y_val)
                if curve.is_on_curve(point):
                    points.append(point)
                    print(f"({bin(x_val)[2:]}, {bin(y_val)[2:]})", end=" ")
        print("\n")
        if not points:
            print("No points found on the curve!")
            return
        G = (0b1000, 0b10)
        print(f"Base point G = ({bin(G[0])[2:]}, {bin(G[1])[2:]})")
        order = curve.point_order(G)
        print(f"Order of base point G: {order}")
        self.ecc_gf2n.set_curve(a, b, irreducible_poly, n, G, order)
        P = points[1] if len(points) > 1 else G
        Q = points[2] if len(points) > 2 else G
        print(f"P = ({bin(P[0])[2:]}, {bin(P[1])[2:]})")
        print(f"Q = ({bin(Q[0])[2:]}, {bin(Q[1])[2:]})")
        P_plus_Q = curve.add_points(P, Q)
        print(f"P + Q = {P_plus_Q if P_plus_Q else 'Point at infinity'}")
        P_doubled = curve.add_points(P, P)
        print(f"2P = {P_doubled if P_doubled else 'Point at infinity'}")
        test_point = (0b1, 0b110)
        doubled_test = curve.add_points(test_point, test_point)
        print(f"Doubling test for {test_point}: 2*({bin(test_point[0])[2:]}, {bin(test_point[1])[2:]}) = "
              f"{doubled_test if doubled_test else 'Point at infinity'}")
        k = 3
        kP = curve.multiply_point(P, k)
        print(f"{k}P = {kP if kP else 'Point at infinity'}")
        print("\nTesting ECDH key exchange...")
        alice_private, alice_public = self.ecc_gf2n.generate_keypair()
        print(f"Alice's private key: {alice_private}")
        print(f"Alice's public key: ({bin(alice_public[0])[2:]}, {bin(alice_public[1])[2:]})")
        bob_private, bob_public = self.ecc_gf2n.generate_keypair()
        print(f"Bob's private key: {bob_private}")
        print(f"Bob's public key: ({bin(bob_public[0])[2:]}, {bin(bob_public[1])[2:]})")
        alice_shared = self.ecc_gf2n.compute_shared_secret(alice_private, bob_public)
        bob_shared = self.ecc_gf2n.compute_shared_secret(bob_private, alice_public)
        print(f"Alice's computed shared secret: {bin(alice_shared)[2:]}")
        print(f"Bob's computed shared secret: {bin(bob_shared)[2:]}")
        print(f"Shared secrets match: {alice_shared == bob_shared}")
        
        print("\nTesting encryption/decryption...")
        message = "Hello, ECC!"
        print(f"Original message: {message}")
        
        # Set the recipient key before encryption (Bob's public key)
        self.ecc_gf2n.set_recipient_key(bob_public)
        
        # Using Alice's private key for encryption
        self.ecc_gf2n.key = alice_private
        
        ciphertext, metrics = self.ecc_gf2n.encrypt(message)
        print(f"Ciphertext: (({bin(ciphertext[0][0])[2:]}, {bin(ciphertext[0][1])[2:]}), {bin(ciphertext[1])[2:]})")
        print(f"Encryption metrics: {metrics}")
        
        # Set Bob's private key for decryption
        self.ecc_gf2n.key = bob_private
        
        decrypted, metrics = self.ecc_gf2n.decrypt(ciphertext)
        print(f"Decrypted message: {decrypted}")
        print(f"Decryption metrics: {metrics}")
        
        # Verify the decryption was successful
        message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16) % (2**self.ecc_gf2n.curve.degree)
        print(f"Original message hash: {bin(message_hash)[2:]}")
        print(f"Decryption successful: {str(message_hash) == decrypted}")
    
    def test_secp256k1(self):
        print("\n===== Testing secp256k1 Curve =====")
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        a = 0
        b = 7
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        G = (Gx, Gy)
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        curve = EllipticCurveGFp(a, b, p)
        print(f"Base point G is on the curve: {curve.is_on_curve(G)}")
        self.ecc_gfp.set_curve(a, b, p, G, n)
        print("\nTesting ECDH key exchange...")
        alice_private, alice_public = self.ecc_gfp.generate_keypair()
        print(f"Alice's private key (truncated): {hex(alice_private)[:10]}...")
        print(f"Alice's public key (truncated): ({hex(alice_public[0])[:10]}..., {hex(alice_public[1])[:10]}...)")
        bob_private, bob_public = self.ecc_gfp.generate_keypair()
        print(f"Bob's private key (truncated): {hex(bob_private)[:10]}...")
        print(f"Bob's public key (truncated): ({hex(bob_public[0])[:10]}..., {hex(bob_public[1])[:10]}...)")
        alice_shared = self.ecc_gfp.compute_shared_secret(alice_private, bob_public)
        bob_shared = self.ecc_gfp.compute_shared_secret(bob_private, alice_public)
        print(f"Shared secrets match: {alice_shared == bob_shared}")
        alice_key = hashlib.sha256(str(alice_shared).encode()).hexdigest()
        bob_key = hashlib.sha256(str(bob_shared).encode()).hexdigest()
        print(f"Alice's derived key (truncated): {alice_key[:10]}...")
        print(f"Bob's derived key (truncated): {bob_key[:10]}...")
        print(f"Derived keys match: {alice_key == bob_key}")
    
    def test_curve25519(self):
        print("\n===== Curve25519 Parameters =====")
        p = 2**255 - 19
        A = 486662
        B = 1
        print(f"Field prime p = 2^255 - 19 = {p}")
        print(f"Curve equation: y^2 = x^3 + {A}x^2 + x mod {p}")
        print("Note: Curve25519 is typically used in Montgomery form for efficient x-coordinate-only operations.")
    
    def test_binary_curve(self):
        print("\n===== Testing a Small Binary Curve =====")
        degree = 4
        irreducible_poly = 0b10011
        a = 0b0001
        b = 0b0001
        curve = EllipticCurveGF2n(a, b, irreducible_poly, degree)
        for x in range(1 << degree):
            for y in range(1 << degree):
                if curve.is_on_curve((x, y)):
                    G = (x, y)
                    print(f"Found point G = ({bin(G[0])[2:]}, {bin(G[1])[2:]})")
                    break
            else:
                continue
            break
        n = curve.point_order(G)
        self.ecc_gf2n.set_curve(a, b, irreducible_poly, degree, G, n)
        G2 = curve.add_points(G, G)
        print(f"2G = {G2 if G2 else 'Point at infinity'}")
        G3 = curve.add_points(G2, G)
        print(f"3G = {G3 if G3 else 'Point at infinity'}")
    
    def run_all_tests(self):
        print("======================================")
        print("Elliptic Curve Cryptography Tests")
        print("======================================")
        self.test_gfp()
        self.test_gf2n()
        self.test_secp256k1()
        self.test_curve25519()
        self.test_binary_curve()

# Main Function
def main():
    tester = ECCTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()