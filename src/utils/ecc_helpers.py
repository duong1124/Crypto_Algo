import random
import hashlib

def mod_inverse(a, m):
    """
    Find the modular multiplicative inverse of 'a' modulo 'm' using the Extended Euclidean Algorithm.
    Returns x such that (a * x) % m == 1 or None if the inverse doesn't exist.
    """
    if m == 1:
        return 0
    
    # Initialize the Extended Euclidean Algorithm
    m0, a0 = m, a
    y, x = 0, 1
    
    while a > 1:
        # q is quotient
        q = a // m
        
        # Update m and a
        m, a = a % m, m
        
        # Update x and y
        x, y = y, x - q * y
    
    # Make x positive
    if x < 0:
        x += m0
        
    return x

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm to find gcd(a, b) and Bézout coefficients x, y
    such that ax + by = gcd(a, b)
    """
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

class FieldElementGFp:
    """
    Class representing an element in the GF(p) field.
    """
    def __init__(self, value, prime):
        """Initialize with a value and the prime modulus."""
        if value >= prime or value < 0:
            self.value = value % prime
        else:
            self.value = value
        self.prime = prime
    
    def __add__(self, other):
        """Add two field elements."""
        if self.prime != other.prime:
            raise ValueError("Cannot add elements from different fields")
        result = (self.value + other.value) % self.prime
        return FieldElementGFp(result, self.prime)
    
    def __sub__(self, other):
        """Subtract two field elements."""
        if self.prime != other.prime:
            raise ValueError("Cannot subtract elements from different fields")
        result = (self.value - other.value) % self.prime
        return FieldElementGFp(result, self.prime)
    
    def __mul__(self, other):
        """Multiply two field elements."""
        if self.prime != other.prime:
            raise ValueError("Cannot multiply elements from different fields")
        result = (self.value * other.value) % self.prime
        return FieldElementGFp(result, self.prime)
    
    def __truediv__(self, other):
        """Divide two field elements."""
        if self.prime != other.prime:
            raise ValueError("Cannot divide elements from different fields")
        
        # Find the modular multiplicative inverse of other
        inverse = mod_inverse(other.value, self.prime)
        if inverse is None:
            raise ZeroDivisionError(f"Element {other.value} has no multiplicative inverse in GF({self.prime})")
        
        result = (self.value * inverse) % self.prime
        return FieldElementGFp(result, self.prime)
    
    def __pow__(self, exponent):
        """Raise the field element to a power."""
        exponent = exponent % (self.prime - 1)  # Fermat's Little Theorem
        result = pow(self.value, exponent, self.prime)
        return FieldElementGFp(result, self.prime)
    
    def __eq__(self, other):
        """Check if two field elements are equal."""
        if other is None:
            return False
        return self.value == other.value and self.prime == other.prime
    
    def __repr__(self):
        """String representation of the field element."""
        return f"FieldElement({self.value})_GF({self.prime})"

class EllipticCurveGFp:
    """
    Class representing an Elliptic Curve over GF(p) in the form y^2 = x^3 + ax + b
    """
    def __init__(self, a, b, p):
        """Initialize with curve parameters a, b and prime p."""
        self.a = FieldElementGFp(a, p)
        self.b = FieldElementGFp(b, p)
        self.p = p
        
        # Check that the curve is non-singular
        # Discriminant Δ = -16(4a^3 + 27b^2) must not be 0
        delta = -16 * (4 * pow(a, 3) + 27 * pow(b, 2)) % p
        if delta == 0:
            raise ValueError("The curve is singular")
    
    def is_on_curve(self, point):
        """Check if a point lies on the curve."""
        if point is None:  # Point at infinity
            return True
        
        if not isinstance(point, tuple) or len(point) != 2:
            return False  # Not a valid point format
            
        x, y = point
        # Check if y^2 = x^3 + ax + b (mod p)
        left = FieldElementGFp(y, self.p) ** 2
        right = (FieldElementGFp(x, self.p) ** 3) + (self.a * FieldElementGFp(x, self.p)) + self.b
        
        return left == right
    
    def add_points(self, p1, p2):
        """Add two points on the curve."""
        # Handle point at infinity (None represents the point at infinity)
        if p1 is None:
            return p2
        if p2 is None:
            return p1
            
        # Safety check for point formats
        if not isinstance(p1, tuple) or len(p1) != 2:
            raise TypeError(f"Expected point p1 to be a tuple (x,y), got {type(p1)}")
        if not isinstance(p2, tuple) or len(p2) != 2:
            raise TypeError(f"Expected point p2 to be a tuple (x,y), got {type(p2)}")
        
        x1, y1 = p1
        x2, y2 = p2
        
        # Check if points are on the curve
        if not self.is_on_curve(p1) or not self.is_on_curve(p2):
            raise ValueError("Points must be on the curve")
        
        # Convert to field elements
        x1 = FieldElementGFp(x1, self.p)
        y1 = FieldElementGFp(y1, self.p)
        x2 = FieldElementGFp(x2, self.p)
        y2 = FieldElementGFp(y2, self.p)
        
        # Case 1: P1 = -P2, return point at infinity
        if x1 == x2 and y1 == FieldElementGFp(self.p - y2.value, self.p):
            return None
        
        # Case 2: P1 = P2, use the tangent formula
        if x1 == x2 and y1 == y2:
            # Avoid division by zero
            if y1.value == 0:
                return None
            
            # Slope of the tangent line
            m = (x1 ** 2 * FieldElementGFp(3, self.p) + self.a) / (y1 * FieldElementGFp(2, self.p))
        
        # Case 3: Different points, use the secant formula
        else:
            # Avoid division by zero
            if x1 == x2:  # This shouldn't happen if we already checked P1 = -P2
                return None
                
            # Slope of the line through P1 and P2
            m = (y2 - y1) / (x2 - x1)
        
        # Calculate the new point
        x3 = m ** 2 - x1 - x2
        y3 = m * (x1 - x3) - y1
        
        return (x3.value, y3.value)
    
    def multiply_point(self, point, scalar):
        """Multiply a point by a scalar using the double-and-add algorithm."""
        # Handle invalid inputs
        if point is None:
            return None
            
        if not isinstance(point, tuple) or len(point) != 2:
            raise TypeError(f"Expected point to be a tuple (x,y), got {type(point)}")
            
        if not isinstance(scalar, int):
            raise TypeError(f"Expected scalar to be an integer, got {type(scalar)}")
        
        # Handle negation
        if scalar < 0:
            scalar = -scalar
            point = (point[0], self.p - point[1])  # Negate the y-coordinate
            
        if scalar == 0:
            return None  # 0*P = point at infinity
        
        result = None  # Initialize with the point at infinity
        addend = point
        
        while scalar:
            if scalar & 1:  # If the bit is set
                try:
                    result = self.add_points(result, addend)
                except (TypeError, ValueError) as e:
                    print(f"Error adding points during scalar multiplication: {e}")
                    return None
            
            # Double the point
            if addend is not None:
                try:
                    addend = self.add_points(addend, addend)
                except (TypeError, ValueError) as e:
                    print(f"Error doubling point during scalar multiplication: {e}")
                    addend = None
            
            scalar >>= 1  # Right shift by 1 (integer division by 2)
        
        return result
    
class FieldElementGF2n:
    """
    Class representing an element in GF(2^n) field.
    Elements are represented as integers, but operations are bitwise.
    """
    def __init__(self, value, irreducible_poly, degree):
        """
        Initialize with a value and the irreducible polynomial.
        
        Args:
            value (int): The value to represent in the field
            irreducible_poly (int): The irreducible polynomial that defines the field
            degree (int): The degree of the field extension (n in 2^n)
        """
        self.value = value
        self.irreducible_poly = irreducible_poly
        self.degree = degree
        self.modulus = 2**degree
    
    def __add__(self, other):
        """Add (XOR) two field elements."""
        if self.irreducible_poly != other.irreducible_poly:
            raise ValueError("Cannot add elements from different fields")
        return FieldElementGF2n(self.value ^ other.value, self.irreducible_poly, self.degree)
    
    def __sub__(self, other):
        """Subtract (XOR, same as add) two field elements."""
        return self.__add__(other)
    
    def __mul__(self, other):
        """Multiply two field elements."""
        if self.irreducible_poly != other.irreducible_poly:
            raise ValueError("Cannot multiply elements from different fields")
        
        a = self.value
        b = other.value
        p = self.irreducible_poly
        m = self.degree
        
        result = 0
        while b:
            if b & 1:  # If the LSB of b is set
                result ^= a
            
            a <<= 1  # a = a * 2
            if a & (1 << m):  # If degree of a becomes >= m
                a ^= p  # Reduce using the irreducible polynomial
            
            b >>= 1  # Right shift b by 1 (divide by 2)
        
        return FieldElementGF2n(result, self.irreducible_poly, self.degree)
    
    def inverse(self):
        """
        Find the multiplicative inverse using Extended Euclidean Algorithm for polynomials.
        """
        if self.value == 0:
            raise ZeroDivisionError("Zero has no multiplicative inverse")
        
        # Initialize for the Extended Euclidean Algorithm
        r0 = self.irreducible_poly
        r1 = self.value
        s0, s1 = 0, 1
        t0, t1 = 1, 0
        
        while r1 != 0:
            # Binary division to get quotient and remainder
            # In GF(2^n), we don't have regular division, but we can use bitwise operations
            degree_diff = bit_length(r0) - bit_length(r1)
            
            if degree_diff < 0:
                # Swap if r1 has higher degree than r0
                r0, r1 = r1, r0
                s0, s1 = s1, s0
                t0, t1 = t1, t0
                degree_diff = -degree_diff
            
            if degree_diff == 0:
                # They're both the same degree, so we need to subtract once
                r0 ^= r1
                s0 ^= s1
                t0 ^= t1
            else:
                # Compute r0 = r0 XOR (r1 << degree_diff)
                r0 ^= r1 << degree_diff
                s0 ^= s1 << degree_diff
                t0 ^= t1 << degree_diff
        
        # Return the result modulo the field size
        return FieldElementGF2n(s0 % self.modulus, self.irreducible_poly, self.degree)
    
    def __truediv__(self, other):
        """Divide two field elements."""
        return self * other.inverse()
    
    def __pow__(self, exponent):
        """Raise the field element to a power using square-and-multiply algorithm."""
        if exponent == 0:
            return FieldElementGF2n(1, self.irreducible_poly, self.degree)
        
        base = self
        result = FieldElementGF2n(1, self.irreducible_poly, self.degree)
        
        while exponent > 0:
            if exponent & 1:  # If the bit is set
                result = result * base
            
            base = base * base  # Square the base
            exponent >>= 1  # Right shift by 1 (integer division by 2)
        
        return result
    
    def __eq__(self, other):
        """Check if two field elements are equal."""
        if other is None:
            return False
        return (self.value == other.value and 
                self.irreducible_poly == other.irreducible_poly and 
                self.degree == other.degree)
    
    def __repr__(self):
        """String representation of the field element."""
        return f"FieldElement({bin(self.value)[2:]})_GF(2^{self.degree})"


def bit_length(n):
    """Return the bit length of an integer."""
    return n.bit_length()

class EllipticCurveGF2n:
    """
    Class representing an Elliptic Curve over GF(2^n) in the form y^2 + xy = x^3 + ax^2 + b
    """
    def __init__(self, a, b, irreducible_poly, degree):
        """
        Initialize with curve parameters a, b, the irreducible polynomial, and the degree of the field.
        """
        self.irreducible_poly = irreducible_poly
        self.degree = degree
        self.a = FieldElementGF2n(a, irreducible_poly, degree)
        self.b = FieldElementGF2n(b, irreducible_poly, degree)
        
        # Check that the curve is non-singular
        # For a curve in the form y^2 + xy = x^3 + ax^2 + b, the discriminant is b
        if b == 0:
            raise ValueError("The curve is singular")
    
    def is_on_curve(self, point):
        """Check if a point lies on the curve."""
        if point is None:  # Point at infinity
            return True
        
        if not isinstance(point, tuple) or len(point) != 2:
            return False  # Not a valid point format
            
        x, y = point
        x = FieldElementGF2n(x, self.irreducible_poly, self.degree)
        y = FieldElementGF2n(y, self.irreducible_poly, self.degree)
        
        # Check equation: y^2 + xy = x^3 + ax^2 + b
        left = (y * y) + (x * y)
        right = (x * x * x) + (self.a * x * x) + self.b
        
        return left == right
    
    def add_points(self, p1, p2):
        """Add two points on the curve."""
        # Handle point at infinity (None represents the point at infinity)
        if p1 is None:
            return p2
        if p2 is None:
            return p1
            
        # Safety check for point formats
        if not isinstance(p1, tuple) or len(p1) != 2:
            raise TypeError(f"Expected point p1 to be a tuple (x,y), got {type(p1)}")
        if not isinstance(p2, tuple) or len(p2) != 2:
            raise TypeError(f"Expected point p2 to be a tuple (x,y), got {type(p2)}")
            
        x1, y1 = p1
        x2, y2 = p2
        
        # Check if points are on the curve
        if not self.is_on_curve(p1) or not self.is_on_curve(p2):
            raise ValueError("Points must be on the curve")
        
        # Convert to field elements
        x1 = FieldElementGF2n(x1, self.irreducible_poly, self.degree)
        y1 = FieldElementGF2n(y1, self.irreducible_poly, self.degree)
        x2 = FieldElementGF2n(x2, self.irreducible_poly, self.degree)
        y2 = FieldElementGF2n(y2, self.irreducible_poly, self.degree)
        
        # Case 1: P1 = P2, use the doubling formula
        if x1 == x2:
            # If y1 = y2 = 0 or x1 = 0, return point at infinity
            if y1.value == 0 or x1.value == 0:
                return None
            
            # If x1 = x2 but y1 != y2, then P2 = -P1, so P1 + P2 = O
            if y1 != (x1 + y2):
                return None
            
            # Formula for doubling:
            # λ = x1 + y1/x1
            # Note: Division in binary field is multiplication by inverse
            try:
                x1_inverse = x1.inverse()
                lambda_val = x1 + (y1 * x1_inverse)
                
                # x3 = λ^2 + λ + a
                x3 = (lambda_val * lambda_val) + lambda_val + self.a
                
                # y3 = x1^2 + λ*x3 + x3
                y3 = (x1 * x1) + (lambda_val * x3) + x3
                
                return (x3.value, y3.value)
            except Exception as e:
                print(f"Error during point doubling: {e}")
                return None
        
        # Case 2: P1 != P2, use the addition formula
        else:
            # If x1 = x2, points are inverses of each other, return point at infinity
            # This should never happen in GF(2^n) if x1 == x2 but was caught above
            if x1 == x2:
                return None
                
            try:
                # λ = (y1 + y2)/(x1 + x2)
                x_sum = x1 + x2
                if x_sum.value == 0:
                    return None  # Division by zero
                    
                lambda_val = (y1 + y2) / x_sum
                
                # x3 = λ^2 + λ + x1 + x2 + a
                x3 = (lambda_val * lambda_val) + lambda_val + x1 + x2 + self.a
                
                # y3 = λ(x1 + x3) + x3 + y1
                y3 = (lambda_val * (x1 + x3)) + x3 + y1
                
                return (x3.value, y3.value)
            except Exception as e:
                print(f"Error during point addition: {e}")
                return None
    
    def multiply_point(self, point, scalar):
        """Multiply a point by a scalar using the double-and-add algorithm."""
        # Handle invalid inputs
        if point is None:
            return None
            
        if not isinstance(point, tuple) or len(point) != 2:
            raise TypeError(f"Expected point to be a tuple (x,y), got {type(point)}")
            
        if not isinstance(scalar, int):
            raise TypeError(f"Expected scalar to be an integer, got {type(scalar)}")
        
        # Handle negation (though in GF(2^n), -P = P so this may not apply)
        if scalar < 0:
            scalar = -scalar
            # In GF(2^n), -P = (x, x+y) for a point P = (x,y)
            x, y = point
            point = (x, x ^ y)  # XOR for binary field addition
        
        if scalar == 0:
            return None  # 0*P = point at infinity
        
        result = None  # Initialize with the point at infinity
        addend = point
        
        while scalar:
            if scalar & 1:  # If the bit is set
                try:
                    result = self.add_points(result, addend)
                except (TypeError, ValueError) as e:
                    print(f"Error adding points during scalar multiplication: {e}")
                    return None
            
            # Double the point
            if addend is not None:
                try:
                    addend = self.add_points(addend, addend)
                except (TypeError, ValueError) as e:
                    print(f"Error doubling point during scalar multiplication: {e}")
                    addend = None
            else:
                break  # If we reach the point at infinity, further doubling is pointless
                
            scalar >>= 1  # Right shift by 1 (integer division by 2)
        
        return result
    
    def point_order(self, point):
        """Compute the order of a point on the curve."""
        if point is None:
            return 1
        
        print(f"Computing order for point {point}")
        current = point
        order = 1
        max_order = 2**(self.degree) + 1  # Max possible order for the curve
        
        while current is not None and order <= max_order:
            order += 1
            current = self.add_points(current, point)
            if current == point:  # Detect cycles other than going to infinity
                print(f"Cycle detected at order {order}")
                return order
                
        if current is None:
            print(f"Computed order: {order}")
            return order
            
        if order > max_order:
            raise ValueError(f"Point order computation failed: exceeded maximum order {max_order}")
        
        return order