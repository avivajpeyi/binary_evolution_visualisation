import glob
import os
import unittest
import shutil
from binary_evolution_visualiser.visualiser import BinaryVisualiser


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.outdir = "test_out"
        os.makedirs(self.outdir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.outdir):
            shutil.rmtree(self.outdir)

    def test_image_generation(self):
        visualiser = BinaryVisualiser(m1=1, m2=2, e=0.4)
        outfilename = os.path.join(self.outdir, "test.gif")
        visualiser.render(outfilename)
        files = glob.glob(os.path.join(self.outdir, "*.png"))
        self.assertTrue(len(files) > 0)
        self.assertTrue(os.path.exists(outfilename))
        shutil.move(outfilename, os.path.basename(outfilename))

    def test_simple_trajectory(self):
        visualiser = BinaryVisualiser(m1=1, m2=2, e=0.4)
        visualiser.plot_trajectory(self.outdir)
        shutil.move(f"{self.outdir}/trajectory.png", "trajectory.png")


if __name__ == "__main__":
    unittest.main()
