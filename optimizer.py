from math import cos
import matplotlib.pyplot as plt
from itertools import accumulate
from functools import reduce
import operator, os

def clamp(x, a, b):
    return min(max(x, a), b)

def lerp(a, b, x):
    return a + x * (b - a)

class Optimizer:
    MIN, MAX = 0, 1

    def __init__(𝕊, efficency_curve, starting_precentage=0.5, power_gain=2, power_draw=1, max_power=10, dt=0.05):
        # Note to 𝕊: apply some smoothing/lienenicy to efficency_curve
        𝕊.starting_precentage = starting_precentage
        𝕊.Pi = starting_precentage * max_power
        𝕊.Pe = efficency_curve
        𝕊.Pg = power_gain
        𝕊.Pd = power_draw
        𝕊.Pm = max_power
        𝕊.dt = dt
        𝕊.Pa = [True] * len(𝕊.Pe)
        𝕊.max_p_integral = 𝕊.compute_p_integral()

    def clamp_battery(𝕊, v):
        return clamp(v, 0, 𝕊.Pm)

    def mPe(𝕊, i):
        return 𝕊.Pe[i] * 𝕊.Pa[i]

    def integrate_gain(𝕊, p1, p2):
        return reduce(
            operator.add,
            (𝕊.mPe(x)*𝕊.Pg*𝕊.dt for x in range(p1, p2)), 0)

    def compute_gain_integral(𝕊, p1, p2, C=0):
        return list(accumulate(
            (𝕊.mPe(x)*𝕊.Pg*𝕊.dt for x in range(p1, p2)),
            operator.add,
            initial=C))

    def integrate_loss(𝕊, p1, p2):
        return 𝕊.Pd * 𝕊.dt*(p2 - p1)

    def compute_p_integral(𝕊):
        return list(accumulate(
            (𝕊.dt*(𝕊.mPe(x)*𝕊.Pg-𝕊.Pd) for x in range(1, len(𝕊.Pe))),
            lambda a, b: 𝕊.clamp_battery(a+b),
            initial=𝕊.Pi))

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

    def find_split_point(𝕊, p1, p2, target=None):
        target = target or 𝕊.Pm

        gain_cache = 𝕊.compute_gain_integral(0, len(𝕊.Pe))
        start_val = 𝕊.max_p_integral[p1]

        for i in range(p1, p2):
            delta_loss = 𝕊.integrate_loss(p1, i)
            current_total = start_val - delta_loss
            if current_total < 0.2 * 𝕊.Pm:
                return i - 1

            total = start_val + \
                (gain_cache[p2] - gain_cache[i]) - 𝕊.integrate_loss(p1, p2)

            if total < target:
                return i - 1
        return p2

    def find_peak_reduce_split_point(𝕊, p1, p2, p3):  # 0→1→1
        gain_cache = 𝕊.compute_gain_integral(0, len(𝕊.Pe))
        start_val = 𝕊.max_p_integral[p1]
        for i in reversed(range(p1, p2)):
            val = start_val + \
                (gain_cache[i] - gain_cache[p1]) - 𝕊.integrate_loss(p1, i)
            if val < 0.8 * 𝕊.Pm:
                marker = i + 1
                break
        else:
            raise Exception()
        return marker, 𝕊.find_split_point(marker, p3)

    def flatten_tops(𝕊):
        extremes = 𝕊.compute_extremes(𝕊.max_p_integral, 𝕊.Pm)
        skip = 0
        for i, (x, T) in enumerate(extremes):
            if skip:
                skip -= 1
                continue

            if i == len(extremes) - 1:
                break
            n_x, n_T = extremes[i + 1]

            if T == Optimizer.MAX == n_T:
                sp = j.find_split_point(x, n_x)
                𝕊.Pa[x+1:sp] = [False] * (sp - x)
                skip = 1
            elif T == Optimizer.MIN == n_T:
                if all(𝕊.max_p_integral[k] <= 0 for k in range(x, n_x)):
                    𝕊.Pa[x+1:n_x] = [False] * (n_x-x)
                    skip = 1

        𝕊.max_p_integral = 𝕊.compute_p_integral()

    def merge_tops(𝕊):
        extremes = 𝕊.compute_extremes(𝕊.max_p_integral, 𝕊.Pm)
        if len(extremes):
            extremes.insert(0, [0, 0])
        
        while extremes and (e := extremes.pop(0)):
            if e[1] == Optimizer.MIN:
                j = []
                while extremes and (k := extremes.pop(0)):
                    if k[1] == Optimizer.MAX:
                        j.append(k[0])
                        continue
                    extremes.insert(0, k)
                    break
                if len(j) >= 2:
                    p1, p2 = 𝕊.find_peak_reduce_split_point(e[0], j[0], j[-1])
                    𝕊.Pa[p1:p2] = [False] * (p2-p1)
                    𝕊.max_p_integral = 𝕊.compute_p_integral()
                    𝕊.merge_tops()

if __name__ == "__main__":
    dt = 0.001
    j = Optimizer([
        0.1*((x*dt)**1/2)*(cos((x*dt))+1) if ((x*dt) % 20) < 5 else 0
        for x in range(int(120 / dt))], dt=dt)
    extremes = j.compute_extremes(j.max_p_integral, j.Pm, True)
    plt.plot(j.max_p_integral)
    plt.scatter(*zip(*extremes))
    j.merge_tops()
    plt.plot(j.max_p_integral)
    plt.plot(*zip(*enumerate(j.Pa)))
    plt.show()