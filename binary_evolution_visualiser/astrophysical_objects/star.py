from typing import Optional

import numpy as np

from .stellar_type import StellarType
from ..math_utils.vector import Vector


class Star:
    def __init__(
        self,
        mass: float,
        radius: Optional[np.ndarray] = None,
        stellar_type: Optional[StellarType] = StellarType.BH,
        luminosity: Optional[np.ndarray] = None,
        effective_temprature: Optional[np.ndarray] = None,
    ):
        self.mass = mass
        self.position = None
        self.velocity = None
        self.radius = radius
        self.stellar_type = stellar_type
        self.luminosity = luminosity
        self.effective_temprature = effective_temprature

    def initialise_vectors(self, num_steps):
        self.position = Vector.list_of_vectors(num_steps)
        self.velocity = Vector.list_of_vectors(num_steps)
        self.time = np.zeros(num_steps, np.float64)

    @property
    def positions(self):
        return Vector.unrap_list_of_vectors_to_data(self.position)

    @property
    def velocities(self):
        return Vector.unrap_list_of_vectors_to_data(self.velocity)

    def __str__(self):
        return f"Star: {self.stellar_type}"
