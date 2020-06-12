"""
Visualises the evolution of a binary system
"""
from .astrophysical_objects import BinarySystem


class BinaryVisualiser:
    def __init__(self, binary_system: BinarySystem):
        self.binary_system = binary_system

    def render(self, outfile: str):
        raise NotImplementedError
