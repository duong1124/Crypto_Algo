from utils.sha512_helpers import *
from utils.helpers import *

class SHA_512():
    def __init__(self, verbose = 0):
        self.verbose = verbose
        self.numRounds = NUM_ROUNDS
        self.H =  H_const
        self.y = 0
        self.x = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.g = 0
        self.h = 0
        self.w = 0
        self.W = [0] * 16
        self.k = 0
        self.K = K_const
        
    def sha512_encrypt(self, block):
        self.sha512_W_schedule(block)
        self.sha512_copy_digest()
        if self.verbose:
            print("State after init:")
            self.sha512_print_state(0)

        for i in range(self.numRounds):
            self.sha512_round(i)
            if self.verbose:
                self.sha512_print_state(i)

        self.sha512_update_digest()
    
    def sha512_copy_digest(self):
        """Update digest after each round"""
        self.a = self.H[0] 
        self.b = self.H[1] 
        self.c = self.H[2] 
        self.d = self.H[3] 
        self.e = self.H[4] 
        self.f = self.H[5] 
        self.g = self.H[6] 
        self.h = self.H[7]


    def sha512_update_digest(self):
        """Update digest after each block"""
        self.H[0] = (self.H[0] + self.a) & MAX_64BIT
        self.H[1] = (self.H[1] + self.b) & MAX_64BIT
        self.H[2] = (self.H[2] + self.c) & MAX_64BIT
        self.H[3] = (self.H[3] + self.d) & MAX_64BIT
        self.H[4] = (self.H[4] + self.e) & MAX_64BIT
        self.H[5] = (self.H[5] + self.f) & MAX_64BIT
        self.H[6] = (self.H[6] + self.g) & MAX_64BIT
        self.H[7] = (self.H[7] + self.h) & MAX_64BIT


    def sha512_print_state(self, round):
        print("State at round 0x%02x:" % round)
        print("y = 0x%016x, x = 0x%016x" % (self.y, self.x))
        print("k  = 0x%016x, w  = 0x%016x" % (self.k,  self.w))
        print("a  = 0x%016x, b  = 0x%016x" % (self.a,  self.b))
        print("c  = 0x%016x, d  = 0x%016x" % (self.c,  self.d))
        print("e  = 0x%016x, f  = 0x%016x" % (self.e,  self.f))
        print("g  = 0x%016x, h  = 0x%016x" % (self.g,  self.h))
        print("")


    def sha512_round(self, round):
        self.k = self.K[round]
        self.w = self.sha512_next_w(round)
        self.y = sha512_Y(self.e, self.f, self.g, self.h, self.k, self.w)
        self.x = sha512_X(self.a, self.b, self.c)
        self.h = self.g
        self.g = self.f
        self.f = self.e
        self.e = (self.d + self.y) & MAX_64BIT
        self.d = self.c
        self.c = self.b
        self.b = self.a
        self.a = (self.y + self.x) & MAX_64BIT


    def sha512_next_w(self, round):
        """Calculating W of each round"""
        if (round < 16):
            return self.W[round]

        else:
            tmp_w = (sha512_delta1(self.W[14]) +
                        self.W[9] + 
                        sha512_delta0(self.W[1]) +
                        self.W[0]) & MAX_64BIT
            for i in range(15):
                self.W[i] = self.W[(i+1)]
            self.W[15] = tmp_w
            return tmp_w

    def sha512_W_schedule(self, block):
        for i in range(16):
            self.W[i] = block[i]
            
    
        
            
        