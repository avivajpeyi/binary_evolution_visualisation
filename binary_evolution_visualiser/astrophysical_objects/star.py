import numpy as np


class Star:
    def __init__(self, mass: np.ndarray):
        self.mass = mass

    def __str__(self):
        return f"{self.mass}"
