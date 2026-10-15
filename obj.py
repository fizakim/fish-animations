import math

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Obj:
    def __init__(self, path):
        self.verts, self.faces = [], []
        for line in open(path):
            kind, *vals = line.split()
            if kind == "v":
                self.verts.append([float(x) for x in vals])
            else:
                self.faces.append([int(i) - 1 for i in vals])

    def tris(self, verts):
        return [[(verts[i][0], verts[i][2], verts[i][1]) for i in f] for f in self.faces]

    def swim(self, time, A=0.3, k=2 * math.pi, omega=6, c=(0, 0, 1)):
        xs = [v[0] for v in self.verts]
        lo, hi = min(xs), max(xs)
        out = []
        for x, y, z in self.verts:
            t = (hi - x) / (hi - lo)
            amp = A * (c[0] + c[1] * t + c[2] * t * t)
            out.append([x, y, z + amp * math.sin(k * t - omega * time)])
        return out

    def view_animation(self, interval=30):
        ax = plt.figure().add_subplot(projection="3d")
        ax.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), zlim=(-1.5, 1.5), box_aspect=(1, 1, 1))
        poly = Poly3DCollection(self.tris(self.verts), facecolors="orange", edgecolors="black")
        ax.add_collection3d(poly)
        anim = FuncAnimation(ax.figure, lambda n: poly.set_verts(self.tris(self.swim(n * interval / 1000))), interval=interval, cache_frame_data=False)
        plt.show()
