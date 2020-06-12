import numpy as np
import tqdm

from .star import Star
from ..math_utils.binary_rk4_solver import BinaryRk4Solver
from ..math_utils.constants import G
from ..math_utils.vector import Vector


class BinarySystem:
    """
    Binary Star System with the center of mass at the origin and using
    Kepler's laws
    """

    def __init__(self, star_1: Star, star_2: Star, a: float, e: float, theta: float):
        """

        :param star_1:
        :param star_2:
        :param a: the semi-major axis of star 2
        :param e: eccentricity
        :param theta: angle to rotate the semi-major axis wrt the observer
        """
        self.star_1 = star_1
        self.star_2 = star_2
        self.a = a
        self.e = e
        self.theta = theta

    @property
    def a1(self):
        """ Semi Major axis a1
        masself.star_1 * a1 == masself.star_2 * a2
         a = a1 + a2
        """
        return self.a / (1.0 + self.star_1.mass / self.star_2.mass)

    @property
    def a2(self):
        """ Semi major axis a2
        a = a1 + a2
        """
        return self.a - self.a1

    @property
    def P(self):
        """Orbital Period
        From Kepler's Law:
        P^2 = 4 pi^2 (a_star1 + a_star2)^3 / (G (M_star1 + M_star2))
        """
        numerator = 4 * np.pi ** 2 * (self.a1 + self.a2) ** 3
        denominator = G * (self.star_1.mass + self.star_2.mass)
        return np.sqrt(numerator / denominator)

    @property
    def v_mu(self):
        """velocity of the reduced mass at perihelion
        http://spiff.rit.edu/classes/phys440/lectures/integrals/integrals.html
        """
        m1, m2 = self.star_1.mass, self.star_2.mass
        non_e_part = G * (m1 + m2) / (self.a1 + self.a2)
        e_part = (1.0 + self.e) / (1.0 - self.e)
        return np.sqrt(non_e_part * e_part)

    # star initialisation values

    @property
    def star_1_init_pos(self):
        """star 1 on the -x axis"""
        return Vector(
            x=-self.a1 * (1.0 - self.e) * np.cos(self.theta),
            y=-self.a1 * (1.0 - self.e) * np.sin(self.theta),
        )

    @property
    def star_2_init_pos(self):
        """star 2 on the +x axis"""
        return Vector(
            x=self.a2 * (1.0 - self.e) * np.cos(self.theta),
            y=self.a2 * (1.0 - self.e) * np.sin(self.theta),
        )

    @property
    def star_2_init_vel(self):
        """v_star2 = (mu/m_star2)*v_mu"""
        m1, m2 = self.star_1.mass, self.star_2.mass
        m_ = m1 / (m1 + m2)
        return Vector(
            x=m_ * self.v_mu * np.sin(self.theta) * -1.0,
            y=m_ * self.v_mu * np.cos(self.theta),
        )

    @property
    def star_1_init_vel(self):
        """v_star1 = (mu/m_star1)*v_mu"""
        m1, m2 = self.star_1.mass, self.star_2.mass
        m_ = m2 / (m1 + m2)
        return Vector(
            x=m_ * self.v_mu * np.sin(self.theta),
            y=m_ * self.v_mu * np.cos(self.theta) * -1.0,
        )

    def __str__(self):
        return f"self.star_1:{self.star_1}, self.star_2:{self.star_2}"

    def initialise_stars(self, nsteps, t):
        self.star_1.initialise_vectors(nsteps + 1)
        self.star_2.initialise_vectors(nsteps + 1)
        self.update_stars(
            n=0,
            t=t,
            r1=self.star_1_init_pos,
            r2=self.star_2_init_pos,
            v1=self.star_1_init_vel,
            v2=self.star_2_init_vel,
        )

    def update_stars(self, n, r1, r2, v1, v2, t):
        self.star_1.position[n].assign(r1)
        self.star_1.velocity[n].assign(v1)
        self.star_2.position[n].assign(r2)
        self.star_2.velocity[n].assign(v2)
        self.star_1.time[n] = self.star_2.time[n] = t

    def evolve(self, dt, tmax):
        """ evolve our system to tmax using a stepsize dt """

        t = 0.0
        nsteps = int(tmax / dt)
        self.initialise_stars(nsteps, t)

        rk4_solver = BinaryRk4Solver(
            init_r1=self.star_1_init_pos,
            init_r2=self.star_2_init_pos,
            init_v1=self.star_1_init_vel,
            init_v2=self.star_2_init_vel,
            m1=self.star_1.mass,
            m2=self.star_2.mass,
            dt=dt,
        )

        progress_bar = tqdm.tqdm(range(1, nsteps + 1))
        progress_bar.set_description("Evolving Binaries")
        for n in progress_bar:
            rk4_solver.step_forward()
            t = t + dt
            self.update_stars(
                n=n,
                r1=Vector(x=rk4_solver.y[0], y=rk4_solver.y[1]),
                v1=Vector(x=rk4_solver.y[2], y=rk4_solver.y[3]),
                r2=Vector(x=rk4_solver.y[4], y=rk4_solver.y[5]),
                v2=Vector(x=rk4_solver.y[6], y=rk4_solver.y[7]),
                t=t,
            )

    def kinetic_energies(self):
        """
        KE = 0.5 * mass * v * v
        :return:
        """
        raise NotImplementedError

    def potential_energy(self):
        """
        PE = -G * m1 m2 / (r1 -r2)^2
        :return:
        """
        raise NotImplementedError
