class Paper:
    '''
        This class is the abstraction of the real paper, and contains some data
        will be used in the image processing.
    '''

    def __init__(self, height: int, width: int, x_offset: int, y_offset: int):
        self.height = height
        self.width = width
        # TODO: Is x and y offsets based on the paper size? If so, no need to
        # get x and offsets from parameters. Create a function to calculate it.
        self.x_offset = x_offset
        self.y_offset = y_offset
