class Obj:
    def __init__(self, path):
        self.verts, self.faces = [], []
        for line in open(path):
            kind, *vals = line.split()
            if kind == "v":
                self.verts.append([float(x) for x in vals])
            else:
                self.faces.append([int(i) - 1 for i in vals])
