import math

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Obj:
    def __init__(self, path, length=0, side=2, step=1):
        self.length, self.side = length, side
        self.verts, self.faces = [], []
        for line in open(path):
            kind, *vals = line.split() or [None]
            if kind == "v":
                self.verts.append([float(x) for x in vals])
            elif kind == "f":
                self.faces.append([int(i.split("/")[0]) - 1 for i in vals])
        self.faces = self.faces[::step]

    def tris(self, verts):
        return [[(verts[i][0], verts[i][2], verts[i][1]) for i in f] for f in self.faces]

    def swim(self, time, A=0.3, k=2 * math.pi, omega=6, c=(0, 0, 1)):
        xs = [v[self.length] for v in self.verts]
        lo, hi = min(xs), max(xs)
        out = []
        for v in self.verts:
            t = (hi - v[self.length]) / (hi - lo)
            amp = A * (c[0] + c[1] * t + c[2] * t * t)
            p = list(v)
            p[self.side] += amp * math.sin(k * t - omega * time)
            out.append(p)
        return out

    def view_animation(self, interval=30, **swim_args):
        r = max(abs(x) for v in self.verts for x in v)
        ax = plt.figure().add_subplot(projection="3d")
        ax.set(xlim=(-r, r), ylim=(-r, r), zlim=(-r, r), box_aspect=(1, 1, 1))
        poly = Poly3DCollection(self.tris(self.verts), facecolors="orange", edgecolors="black")
        ax.add_collection3d(poly)
        anim = FuncAnimation(ax.figure, lambda n: poly.set_verts(self.tris(self.swim(n * interval / 1000, **swim_args))), interval=interval, cache_frame_data=False)
        plt.show()
