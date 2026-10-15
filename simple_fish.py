import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from obj import Obj


class SimpleFish(Obj):
    def __init__(self, path="objects/simple_fish.obj"):
        super().__init__(path)

    def view(self):
        tris = [[(self.verts[i][0], self.verts[i][2], self.verts[i][1]) for i in f] for f in self.faces]
        ax = plt.figure().add_subplot(projection="3d")
        ax.add_collection3d(Poly3DCollection(tris, facecolors="orange", edgecolors="black"))
        ax.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), zlim=(-1.5, 1.5), box_aspect=(1, 1, 1))
        plt.show()

if __name__== "__main__":
    fish = SimpleFish()
    fish.view()