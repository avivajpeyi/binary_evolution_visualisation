import numpy as np

from .star import Star


class BinarySystem:
    def __init__(
        self,
        star_1: Star,
        star_2: Star,
        time: np.ndarray,
        separation: np.ndarray,
        eccentricity: np.ndarray,
    ):
        """

        :param star_1:
        :param star_2:
        """
        self.star_1 = star_1
        self.star_2 = star_2
        self.time = time
        self.separation = separation
        self.eccentricity = eccentricity

    def __str__(self):
        return f"s1:{self.star_1}, s2:{self.star_2}"
