import numpy as np


class Star:
    def __init__(
        self, mass: np.ndarray, radius, stellar_type, luminosity, effective_temprature
    ):
        self.mass = mass
        self.radius = radius
        self.stellar_type = stellar_type
        self.luminosity = luminosity
        self.effective_temprature = effective_temprature

    def __str__(self):
        return f"{self.mass}"
