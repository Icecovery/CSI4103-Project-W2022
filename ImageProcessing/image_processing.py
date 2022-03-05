import os
import cv2 as cv
import numpy as np

from .paper import Paper
from .image_converter import *
from .path_optimizer import *
from .pixel_to_real_space_converter import *

def image_process(src_image_path: str, paper: Paper, debug=False):
    '''
        @brief Process the source image, and return the real-world coordinates
        of line segments.
    '''

    # read the source image
    src_img = cv.imread(src_image_path)
    image_converter_args = ImageConverterArgs(
        blur_radius=5,
        canny_threshold_1=60,
        canny_threshold_2=10,
        hough_threshold=8,
        aperture_size=3,
        min_line_length=5,
        max_line_gap=5,
        rho=1,
        theta=np.pi/180
    )

    # convert the source image
    image_converter = ImageConverter(src_img, image_converter_args, debug)
    segments = image_converter.convert()

    # optimize the moving path
    optimizer = PathOptimizer()
    optimized_segments = optimizer.optimize(segments, debug=debug, shape=src_img.shape)

    # convert image to real space
    pixel_to_real = PixelToRealSpaceConverter()
    real_space_segments = pixel_to_real.convert(optimized_segments, src_img.shape, 
        (paper.height, paper.width), (paper.x_offset, paper.y_offset), debug=debug)

    return real_space_segments
