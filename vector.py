import math

class Vect2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vect2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self = self + other

    def __sub__(self, other):
        return self + (-other)

    def __isub__(self, other):
        self = self - other

    def __neg__(self):
        return Vect2(-self.x, -self.y)

    def __mul__(self, n):
        self.x *= n
        self.y *= n

    def __imul__(self, other):
        self.x *= other
        self.y *= other

    def __abs__(self):
        return math.dist((0, 0), (self.x, self.y))

    def __repr__(self):
        return f"Vect2({self.x}, {self.y})"

    def __str__(self):
        return f"Vect2({self.x}, {self.y})"

    def tuple(self):
        return self.x, self.y

    def normalize(self):
        norm = abs(self)
        if norm != 0:
            self.x /= norm
            self.y /= norm