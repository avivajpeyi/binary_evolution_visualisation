"""
Parses Compass files and formats them for visualisation
"""
import logging

from .astrophysical_objects import Star, BinarySystem

logging.getLogger().setLevel(logging.INFO)


class CompasHandler:
    def __init__(self, compas_file_name):
        """
        Parses COMPAS file and generates a binary system with its stars
        :param compas_file_name:
        """
        self.binary_system = BinarySystem(star_1=Star(mass=1), star_2=Star(mass=2))
        raise NotImplementedError

    @classmethod
    def get_binary_system_from_compas_file(cls, compas_file_name: str):
        return cls(compas_file_name).binary_system
