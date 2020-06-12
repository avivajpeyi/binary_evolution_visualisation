import unittest

from binary_evolution_visualiser.astrophysical_objects import BinarySystem
from binary_evolution_visualiser.compass_handler import CompasHandler

COMPAS_TEST_FPATH = "tests/COMPAS_Output/Detailed_Output/BSE_Detailed_Output_0.csv"


class TestCompasHandler(unittest.TestCase):
    def setUp(self):
        self.compas_file_path = COMPAS_TEST_FPATH

    def test_compas_file_loaded(self):
        binary_sys = CompasHandler(compas_file_name=self.compas_file_path)
        self.assertIsInstance(binary_sys, BinarySystem)


if __name__ == "__main__":
    unittest.main()
