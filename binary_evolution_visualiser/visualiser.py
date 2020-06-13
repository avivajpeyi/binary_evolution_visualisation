"""
Visualises the evolution of a binary system
"""

import glob
import os
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import tqdm
from PIL import Image
import logging

from .astrophysical_objects import BinarySystem, Star
from .math_utils.constants import M_sun, AU, year

logging.getLogger().setLevel(logging.INFO)


FNAME = "binary_star_mratio={:3.2f}_e={:3.2f}_{:04d}.png"


class BinaryVisualiser:
    def __init__(
        self, m1=1, m2=1, a2=10, e=0.0, tmax: Optional[int] = None, annotate=False
    ):
        """

        :param m1:
        :param m2:
        :param a2:
        :param e:
        :param tmax:
        :param annotate:
        """

        a_star2 = a2 * AU
        a_star1 = (m2 / m1) * a_star2

        # create the binary object
        self.binary_system = BinarySystem(
            star_1=Star(mass=m1 * M_sun),
            star_2=Star(mass=m2 * M_sun),
            a=a_star1 + a_star2,
            e=e,
            theta=np.pi / 6.0,
        )
        self.tmax = tmax
        self.annotate = annotate
        self.evolve_binary_system()

    def evolve_binary_system(self):
        # set the timestep in terms of the orbital period
        self.dt = self.binary_system.P / 360.0
        if self.tmax is None:
            self.tmax = 2.0 * self.binary_system.P
        # evolve the system
        self.binary_system.evolve(self.dt, self.tmax)

    def render(self, outfile: str):
        outdir = os.path.dirname(outfile)
        self.generate_frames(outdir)
        self.plot_trajectory(outdir)
        self.compile_frames(outfile)

    def compile_frames(self, outfile):
        """
        https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
        :return:
        """
        logging.info("Compiling frames into a gif...")
        file_name = FNAME.split("=")[0] + "*.png"
        search_regex = os.path.join(os.path.dirname(outfile), file_name)
        img, *imgs = [Image.open(f) for f in sorted(glob.glob(search_regex))]
        img.save(
            fp=outfile,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=200,
            loop=0,
        )

    def plot_trajectory(self, outdir):
        os.makedirs(outdir, exist_ok=True)

        s1 = self.binary_system.star_1
        s2 = self.binary_system.star_2
        s1_pos, s2_pos = s1.positions, s2.positions

        fig = plt.figure(1)
        fig.clear()

        ax = fig.add_subplot(111)

        plt.subplots_adjust(left=0.025, right=0.975, bottom=0.025, top=0.975)

        ax.set_aspect("equal", "datalim")
        ax.set_axis_off()

        # Center of mass
        ax.scatter([0], [0], s=150, marker="x", color="k")

        if not (s1.mass == s2.mass and self.binary_system.e == 0.0):
            ax.plot(s2_pos["x"], s2_pos["y"], color="C1")

        # plot star 1's orbit
        if not (s1.mass == s2.mass and self.binary_system.e == 0.0):
            ax.plot(s1_pos["x"], s1_pos["y"], color="C0")
        else:
            ax.plot(s1_pos["x"], s1_pos["y"], color="k")

        xmin = 1.05 * min(min(s1_pos["x"]), min(s2_pos["x"]))
        xmax = 1.05 * max(max(s1_pos["x"]), max(s2_pos["x"]))
        ymin = 1.05 * min(min(s1_pos["y"]), min(s2_pos["y"]))
        ymax = 1.05 * max(max(s1_pos["y"]), max(s2_pos["y"]))

        if self.annotate:
            # plot a reference line
            ax.plot([0, 1 * AU], [0.93 * ymin, 0.93 * ymin], color="k")
            ax.text(
                0.5 * AU,
                0.975 * ymin,
                "1 AU",
                horizontalalignment="center",
                verticalalignment="top",
            )

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        fig.set_size_inches(12.8, 7.2)

        plt.tight_layout()

        fname = "trajectory.png"

        plt.savefig(os.path.join(outdir, fname))

    def generate_frames(self, outdir="temp"):
        os.makedirs(outdir, exist_ok=True)
        s1 = self.binary_system.star_1
        s2 = self.binary_system.star_2

        iframe = 0

        # KE1, KE2 = self.binary_system.kinetic_energies()
        # PE = self.binary_system.potential_energy()

        s1_pos, s2_pos = s1.positions, s2.positions

        progress_bar = tqdm.tqdm(range(len(s1.time)))
        progress_bar.set_description("Plotting Binary System")
        for n in progress_bar:

            fig = plt.figure(1)
            fig.clear()

            ax = fig.add_subplot(111)

            plt.subplots_adjust(left=0.025, right=0.975, bottom=0.025, top=0.975)

            ax.set_aspect("equal", "datalim")
            ax.set_axis_off()

            # Center of mass
            ax.scatter([0], [0], s=150, marker="x", color="k")

            # if e = 0 and M_star1 = M_star2, then the orbits lie on top of one
            # another, so plot only a single orbital line.

            # plot star 1's orbit
            symsize = 200
            if not (s1.mass == s2.mass and self.binary_system.e == 0.0):
                ax.plot(s1_pos["x"], s1_pos["y"], color="C0")
            else:
                ax.plot(s1_pos["x"], s1_pos["y"], color="k")
            # plot star 1's position
            ax.scatter(
                [s1_pos["x"][n]], [s1_pos["y"][n]], s=symsize, color="C0", zorder=100
            )

            # plot star 2's orbit
            symsize = 200 * (s1.mass / s2.mass)
            if not (s1.mass == s2.mass and self.binary_system.e == 0.0):
                ax.plot(s2_pos["x"], s2_pos["y"], color="C1")

            # plot star 2's position
            ax.scatter(
                [s2_pos["x"][n]], [s2_pos["y"][n]], s=symsize, color="C1", zorder=100
            )

            if self.annotate:
                # display time
                ax.text(
                    0.05,
                    0.05,
                    "time = {:6.3f} yr".format(s1.time[n] / year),
                    transform=ax.transAxes,
                )

            # display information about stars
            # assumes that M_2 < M_1
            ax.text(
                0.05,
                0.95,
                r"mass ratio: {:3.2f}".format(s1.mass / s2.mass),
                transform=ax.transAxes,
                color="k",
                fontsize="large",
            )
            ax.text(
                0.05,
                0.9,
                r"eccentricity: {:3.2f}".format(self.binary_system.e),
                transform=ax.transAxes,
                color="k",
                fontsize="large",
            )

            # energies
            # if annotate:
            #     # KE 1
            #     sig, ex = convert_to_scientific_notation(KE1[n])
            #     ax.text(0.05, 0.4,
            #             r"$K_1 = {:+4.2f} \times 10^{{{:2d}}}$ erg".format(sig, ex),
            #             transform=ax.transAxes, color="C0")
            #
            #     sig, ex = convert_to_scientific_notation(KE2[n])
            #     ax.text(0.05, 0.35,
            #             r"$K_2 = {:+4.2f} \times 10^{{{:2d}}}$ erg".format(sig, ex),
            #             transform=ax.transAxes, color="C1")
            #
            #     sig, ex = convert_to_scientific_notation(PE[n])
            #     ax.text(0.05, 0.3,
            #             r"$U = {:+4.2f} \times 10^{{{:2d}}}$ erg".format(sig, ex),
            #             transform=ax.transAxes)
            #
            #     sig, ex = convert_to_scientific_notation(KE1[n] + KE2[n] + PE[n])
            #     ax.text(0.05, 0.25,
            #             r"$E = {:+4.2f} \times 10^{{{:2d}}}$ erg".format(sig, ex),
            #             transform=ax.transAxes)

            xmin = 1.05 * min(min(s1_pos["x"]), min(s2_pos["x"]))
            xmax = 1.05 * max(max(s1_pos["x"]), max(s2_pos["x"]))
            ymin = 1.05 * min(min(s1_pos["y"]), min(s2_pos["y"]))
            ymax = 1.05 * max(max(s1_pos["y"]), max(s2_pos["y"]))

            if self.annotate:
                # plot a reference line
                ax.plot([0, 1 * AU], [0.93 * ymin, 0.93 * ymin], color="k")
                ax.text(
                    0.5 * AU,
                    0.975 * ymin,
                    "1 AU",
                    horizontalalignment="center",
                    verticalalignment="top",
                )

            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)

            fig.set_size_inches(12.8, 7.2)

            plt.tight_layout()

            fname = FNAME.format(s1.mass / s2.mass, self.binary_system.e, iframe)

            plt.savefig(os.path.join(outdir, fname))

            iframe += 1
