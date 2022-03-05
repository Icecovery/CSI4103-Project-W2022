import math

class CoordinatesToAnglesConverter:
    '''
        This class is used to convert the coordinates in path.csv to the angles
        of the servos. Use inverse kinematics to do the converting.
    '''

    def __init__(self):
        pass

def coordinate_to_angle(x, y, la, lb):
    ac = math.sqrt(x ** 2 + y ** 2)
    bac = math.acos((la ** 2 + ac ** 2 - lb ** 2) / (2.0 * la * ac))
    yac = math.asin(x / ac)
    yab = (math.pi - yac - bac) if y > 0 else (yac - bac)

    angleA = yab
    angleB = math.acos((la ** 2 + lb ** 2 - ac ** 2) / (2.0 * la * lb))

    return (angleA, angleB)
