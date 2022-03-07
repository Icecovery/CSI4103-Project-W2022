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

def test_coordinate_to_angle():
	# TODO: add more test cases
	EPS = 0.001
	a, b = coordinate_to_angle(100, -100, 100, 100)
	assert pytest.approx(a, EPS) == 0.0
	assert pytest.approx(b, EPS) == math.pi / 2
