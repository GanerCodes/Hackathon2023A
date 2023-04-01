from itertools import accumulate

def clamp(x, a, b):
    return min(max(x, a), b)


class Optimizer:
    MIN, MAX = 0, 1

    def __init__(self, efficency_curve, starting_precentage=0.5, power_gain=2, power_draw=1, max_power=10, dt=0.05):
        # Note to self: apply some smoothing/lienenicy to efficency_curve
        self.Pe = efficency_curve
        self.P0 = starting_precentage * max_power
        self.Pg = power_gain
        self.Pd = power_draw
        self.Pm = max_power
        self.dt = dt
        self.max_p_integral = self.compute_max_p_integral(
            self.Pe, self.P0, self.Pg, self.Pd, self.Pm, self.dt)

    def compute_max_p_integral(_, Pe, P0, Pg, Pd, Pm, dt):
        return tuple(accumulate(
            (dt*(x*Pg-Pd) for x in Pe[1:]),
            lambda a, b: clamp(a+b, 0, Pm),
            initial=P0))

    def compute_extremes(_, max_p_integral, Pm, graph_mode=False):
        extremes = []
        for i, v in enumerate(max_p_integral):
            prev = max_p_integral[i-1] if i > 0 else None
            post = max_p_integral[i+1] if i < len(max_p_integral)-1 else None
            if v == prev == post:
                continue
            if graph_mode:
                if v in (0, Pm):
                    extremes.append((i, v))
            else:
                if v == 0:
                    extremes.append((i, Optimizer.MIN))
                elif v == Pm:
                    extremes.append((i, Optimizer.MAX))
        return extremes

from math import sin
import matplotlib.pyplot as plt
j = Optimizer([0.4*(sin(x/10)+1) for x in range(100)], dt=1)
extremes = j.compute_extremes(j.max_p_integral, j.Pm, True)

plt.plot(j.max_p_integral)
plt.scatter(*zip(*extremes))
plt.show()