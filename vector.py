import math

class Vect2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vect2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __isub__(self, other):
        return self - other

    def __neg__(self):
        return Vect2(-self.x, -self.y)

    def __mul__(self, n):
        return Vect2(self.x * n, self.y * n)

    def __imul__(self, other):
        return Vect2(self.x * other, self.y * other)  
        
    def __abs__(self):
        return math.dist((0, 0), (self.x, self.y))

    def __repr__(self):
        return f"Vect2({self.x}, {self.y})"

    def __str__(self):
        return f"Vect2({self.x}, {self.y})"

    def norm(self):
        return abs(self)

    def tuple(self):
        return self.x, self.y

    def normalized(self):
        norm = abs(self)
        if norm == 0:
            return Vect2()
        return Vect2(self.x / norm, self.y / norm)

    def normalize(self):
        self = self.normalized()
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
        
    def dist(self, other):
        return math.dist(self.tuple(), other.tuple())