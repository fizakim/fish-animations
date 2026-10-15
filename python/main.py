from pathlib import Path
import numpy as np

from obj import Obj

objects = Path(__file__).parent.parent / "objects"

fish = Obj(objects / "simple_fish.obj", 
           amp=lambda t: t**2, 
           freq=1, 
           wl=1)

fish.view_animation(show_spine=True)
