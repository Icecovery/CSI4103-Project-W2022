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

"""
Tests applied with the following arm lengths and offsets:
    A_OFFSET = 38.69
    B_OFFSET = 0.0
    ARM_A_LEN = 160
    ARM_B_LEN = 150
"""
def test_lines_to_instructions():
    EPS = 0.001

    lines = [[[100, 100], [200, 0]], [[50, 50], [141.4214, 0]]]
    instructions = lines_to_instructions(lines)
    print(instructions)

    check_points = [(114.3833, 54.1676), (81.0229, 80.2849), (104.6658, 26.1144), (69.3833, 54.1676)]
    checked = 0
    for inst in instructions:
        if type(inst) is tuple:
            for p in check_points:
                if pytest.approx(inst[0], EPS) == p[0] and pytest.approx(inst[1], EPS) == p[1]:
                    checked += 1

    assert checked == len(check_points)
