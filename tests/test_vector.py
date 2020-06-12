import unittest

import numpy as np

from binary_evolution_visualiser.math_utils.vector import Vector


class TestVector(unittest.TestCase):
    def test_magnitude(self):
        self.assertEqual(Vector(1, 0, 0).magnitude, 1)

    def test_dot_product(self):
        self.assertEqual(Vector(1, 0, 0) * Vector(0, 1, 0), 0)
        self.assertEqual(Vector(1, 0, 0) * 2, Vector(2, 0, 0))

    def test_subtraction(self):
        self.assertEqual(Vector(1, 0, 0) - Vector(1, 0, 0), Vector(0, 0, 0))

    def test_addition(self):
        self.assertEqual(Vector(1, 0, 0) + Vector(1, 0, 0), Vector(2, 0, 0))

    def test_cross_product(self):
        a = np.array([1, 0, 0])
        v1 = Vector(a[0], a[1], a[2])
        b = np.array([0, 1, 0])
        v2 = Vector(b[0], b[1], b[2])
        result = np.cross(a, b)
        vr = Vector(result[0], result[1], result[2])
        self.assertEqual(vr, v1 ** v2)


if __name__ == "__main__":
    unittest.main()
