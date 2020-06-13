import numpy as np

from .constants import G
from .vector import Vector


class BinaryRk4Solver:
    """Potnentially do this with multithreading"""

    def __init__(
        self,
        init_r1: Vector,
        init_v1: Vector,
        init_r2: Vector,
        init_v2: Vector,
        m1: float,
        m2: float,
        dt: float,
    ):
        self.k1 = np.zeros(8, np.float64)
        self.k2 = np.zeros(8, np.float64)
        self.k3 = np.zeros(8, np.float64)
        self.k4 = np.zeros(8, np.float64)
        self.y = np.zeros(8, np.float64)
        self.m1 = m1
        self.m2 = m2
        self.dt = dt
        self.update_y(init_r1, init_v1, init_r2, init_v2)

    def update_y(self, r1, v1, r2, v2):
        self.y[0], self.y[1] = r1.x, r1.y
        self.y[2], self.y[3] = v1.x, v1.y
        self.y[4], self.y[5] = r2.x, r2.y
        self.y[6], self.y[7] = v2.x, v2.y

    def step_forward(self):
        """
        FIXME: Why am i not using t??? t, t + 0.5*dt, etc???
        :return:
        """
        self.k1[:] = self.dt * self.rhs(self.y)
        self.k2[:] = self.dt * self.rhs(self.y[:] + 0.5 * self.k1[:])
        self.k3[:] = self.dt * self.rhs(self.y[:] + 0.5 * self.k2[:])
        self.k4[:] = self.dt * self.rhs(self.y[:] + self.k3[:])
        self.y[:] += (1.0 / 6.0) * (
            self.k1[:] + 2.0 * self.k2[:] + 2.0 * self.k3[:] + self.k4[:]
        )

    def rhs(self, y):
        """ the RHS of our system """
        r1 = Vector(y[0], y[1])
        v1 = Vector(y[2], y[3])
        r2 = Vector(y[4], y[5])
        v2 = Vector(y[6], y[7])
        r_vec = r2 - r1
        r = r_vec.magnitude

        # dr/dt = v
        dr1_dt, dr2_dt = Vector(), Vector()
        dr1_dt.assign(v1)
        dr2_dt.assign(v2)

        # dv/dt = a
        constant = -G / r ** 3
        dv1_dt = constant * self.m1 * (r1 - r2)
        dv2_dt = constant * self.m2 * (r2 - r1)

        f = np.zeros(8, np.float64)
        f[0], f[1] = dr1_dt.x, dr1_dt.y
        f[2], f[3] = dv1_dt.x, dv1_dt.y
        f[4], f[5] = dr1_dt.x, dr1_dt.y
        f[6], f[7] = dv2_dt.x, dv2_dt.y
        return f
