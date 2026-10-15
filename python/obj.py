import math

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Obj:
    def __init__(self, path, length=0, side=2, step=1, amp=lambda t: 0.3 * t**2, freq=1, wl=1):
        self.length = length
        self.side = side
        self.amp = amp
        self.freq = freq
        self.wl = wl
        self.verts = []
        self.faces = []
        for line in open(path):
            parts = line.split()
            if len(parts) == 0:
                continue
            if parts[0] == "v":
                self.verts.append([float(x) for x in parts[1:]])
            elif parts[0] == "f":
                self.faces.append([int(x.split("/")[0]) - 1 for x in parts[1:]])
        self.faces = self.faces[::step]
        xs = [v[length] for v in self.verts]
        self.lo = min(xs)
        self.hi = max(xs)

    def swim(self, time):
        new_verts = []
        for v in self.verts:
            t = (self.hi - v[self.length]) / (self.hi - self.lo)
            p = list(v)
            p[self.side] += self.amp(t) * math.sin(2 * math.pi * (t / self.wl - self.freq * time))
            new_verts.append(p)
        return new_verts

    def spine(self, time, n=50):
        centre = [(min(v[i] for v in self.verts) + max(v[i] for v in self.verts)) / 2 for i in range(3)]
        rest = []
        spine = []
        upper = []
        lower = []
        for i in range(n + 1):
            t = i / n
            a = self.amp(t)
            p = list(centre)
            p[self.length] = self.hi - t * (self.hi - self.lo)
            rest.append(list(p))
            p[self.side] = centre[self.side] + a
            upper.append(list(p))
            p[self.side] = centre[self.side] - a
            lower.append(list(p))
            p[self.side] = centre[self.side] + a * math.sin(2 * math.pi * (t / self.wl - self.freq * time))
            spine.append(list(p))
        return rest, spine, upper, lower

    def triangles(self, verts):
        return [[(verts[i][0], verts[i][2], verts[i][1]) for i in f] for f in self.faces]

    def view_animation(self, show_spine=False):
        r = max(abs(x) for v in self.verts for x in v)
        ax = plt.figure().add_subplot(projection="3d")
        ax.set(xlim=(-r, r), ylim=(-r, r), zlim=(-r, r), box_aspect=(1, 1, 1))
        poly = Poly3DCollection(self.triangles(self.verts), facecolors="orange", edgecolors="black", alpha=0.3 if show_spine else 1)
        ax.add_collection3d(poly)
        lines = [
            ax.plot([], [], [], color="grey", ls="--", zorder=10)[0],
            ax.plot([], [], [], color="red", lw=3, zorder=10)[0],
            ax.plot([], [], [], color="blue", ls=":", zorder=10)[0],
            ax.plot([], [], [], color="blue", ls=":", zorder=10)[0],
        ]

        def update(frame):
            time = frame * 30 / 1000
            poly.set_verts(self.triangles(self.swim(time)))
            if show_spine:
                for line, pts in zip(lines, self.spine(time)):
                    line.set_data_3d([p[0] for p in pts], [p[2] for p in pts], [p[1] for p in pts])

        anim = FuncAnimation(ax.figure, update, interval=30, cache_frame_data=False)
        plt.show()
