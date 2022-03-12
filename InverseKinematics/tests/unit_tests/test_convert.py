import math
import pytest

# start: code to resolve relative imports
import sys
import importlib
from pathlib import Path

from numpy import angle

def import_parents(level=1):
    global __package__
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]
    
    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError: # already removed
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])
    importlib.import_module(__package__) # won't be needed after that

import_parents(level=3) # N = 3
# end: code to resolve relative imports

from ...convert import *

# Refer to ~InverseKinematics\angle-format.png for visualization of angles a and b
def test_coordinate_to_angle():
    EPS = 0.001 

    a, b = coordinate_to_angle(100, -100, 100, 100)
    assert pytest.approx(a, EPS) == 0.0
    assert pytest.approx(b, EPS) == math.pi / 2 

    a, b = coordinate_to_angle(100, 100, 100, 100)
    assert pytest.approx(a, EPS) == math.pi / 2 
    assert pytest.approx(b, EPS) == math.pi / 2 

    a, b = coordinate_to_angle(200, 0, 100, 100)
    assert pytest.approx(a, EPS) == math.pi / 2
    assert pytest.approx(b, EPS) == math.pi

    a, b = coordinate_to_angle(141.421356, 0, 100, 100)
    assert pytest.approx(a, EPS) == math.pi / 4
    assert pytest.approx(b, EPS) == math.pi /2

    a, b = coordinate_to_angle(50, 50, 100, 100)
    assert pytest.approx(a, EPS) == 1.1467655
    assert pytest.approx(b, EPS) == 0.7227342
