import os
import shutil
import unittest

import numpy as np

from binary_evolution_visualiser.visualiser import BinaryVisualiser
from binary_evolution_visualiser.astrophysical_objects import Star, BinarySystem
from binary_evolution_visualiser.astrophysical_objects.stellar_type import StellarType


class TestVisualiser(unittest.TestCase):
    def setUp(self):
        self.outdir = "test"
        os.makedirs(self.outdir, exist_ok=True)

    @staticmethod
    def create_fake_binary(num_points: int) -> BinarySystem:
        return BinarySystem(
            star_1=TestVisualiser.create_fake_star(num_points),
            star_2=TestVisualiser.create_fake_star(num_points),
            time=np.arange(0, 100, num_points),
            separation=np.arange(10, 1, num_points),
            eccentricity=np.zeros(num_points),
        )

    @staticmethod
    def create_fake_star(num_points: int) -> Star:
        return Star(
            mass=np.ones(num_points),
            radius=np.ones(num_points),
            stellar_type=[StellarType.BH for _ in num_points],
            luminosity=np.ones(num_points),
            effective_temprature=np.ones(num_points),
        )

    def tearDown(self):
        if os.path.exists(self.outdir):
            shutil.rmtree(self.outdir)

    def test_visualisation(self):
        render_path = os.path.join(self.outdir, "compas_visualisation.py")
        binary_system = self.create_fake_binary(num_points=100)
        visualiser = BinaryVisualiser(binary_system=binary_system)
        visualiser.render(outfile=render_path)
        self.assertTrue(os.path.isfile(render_path))


if __name__ == "__main__":
    unittest.main()
