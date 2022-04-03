class Paper:
    '''
        This class is the abstraction of the real paper, and contains some data
        will be used in the image processing.
    '''

    def __init__(self, height: int, width: int, x_offset: int, y_offset: int):
        '''
            All the lengths are in mm.
        '''
        self.height = height
        self.width = width
        self.x_offset = x_offset
        self.y_offset = y_offset

# some paper pre-sets
LETTER_PAPER = Paper(279, 216, -50, 140)
