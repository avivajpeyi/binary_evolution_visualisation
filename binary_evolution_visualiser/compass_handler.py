"""
Parses Compass files and formats them for visualisation
"""
from .astrophysical_objects import Star, BinarySystem


class CompasHandler:
    def __init__(self, compas_file_name):
        """
        Parses COMPAS file and generates a binary system with its stars
        :param compas_file_name:
        """
        self.binary_system = BinarySystem(star_1=Star(mass=1), star_2=Star(mass=2))
        raise NotImplementedError
