from typing import Optional

import numpy as np

NP_ZERO = np.float64(0)


class Vector:
    def __init__(
        self,
        x: Optional[np.float64] = NP_ZERO,
        y: Optional[np.float64] = NP_ZERO,
        z: Optional[np.float64] = NP_ZERO,
    ):
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self):
        return np.sqrt(self * self)

    def __str__(self):
        return f"<{self.x:.1f} {self.y:.1f} {self.z:.1f}>"

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rmul__(self, lhs):
        return self * lhs

    def __mul__(self, other):
        """Vector dot product """
        if isinstance(other, Vector):
            # vector multiplication
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            # scalar multiplication
            return Vector(self.x * other, self.y * other, self.z * other)

    def __pow__(self, other):
        """Vector cross product """
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        return False

    def assign(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z

    @staticmethod
    def list_of_vectors(num: int):
        assert isinstance(num, int), f"num {num} not an int"
        return [Vector() for _ in range(num)]

    @staticmethod
    def unrap_list_of_vectors_to_data(list_of_vectors):
        x, y, z = [], [], []
        for v in list_of_vectors:
            x.append(v.x)
            y.append(v.y)
            z.append(v.z)
        return dict(x=x, y=y, z=z)
