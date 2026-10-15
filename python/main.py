from pathlib import Path

from obj import Obj

objects = Path(__file__).parent.parent / "objects"

fish = Obj(objects / "simple_fish.obj")
shark = Obj(objects / "shark.obj", length=2, side=0, step=20)
fish.view_animation(show_spine=True, A=1)
