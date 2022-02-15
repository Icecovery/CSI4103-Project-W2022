import imp
import cv2 as cv
import numpy as np

class ImageConverterArgs:
    '''
        This class is a bundle of geometrical arguments used by ImageConverter class.
    '''

    def __init__(self, blur_radius, canny_threshold_1, canny_threshold_2, hough_threshold, aperture_size, min_line_length, max_line_gap, rho, theta):
        # args to get blur_img
        self.blur_radius = blur_radius
        # args to get canny_img
        self.canny_threshold_1 = canny_threshold_1
        self.canny_threshold_2 = canny_threshold_2
        self.aperture_size = aperture_size
        # args to get line_segs
        self.hough_threshold = hough_threshold
        self.min_line_length = min_line_length
        self.max_line_gap = max_line_gap
        self.rho = rho
        self.theta = theta

        self._calibrate()
    
    def _calibrate(self):
        '''
            @brief private function
        '''
        if self.blur_radius % 2 == 0:
            self.blur_radius += 1 # blur radius must be odd
        if self.aperture_size % 2 == 0:
            self.aperture_size += 1 # aperture size must be odd
        

class ImageConverter:
    def __init__(self, src_img, args: ImageConverterArgs, debug=False):
        '''
            @param src_img: source image
            @param args: an instance of ImageConverterArgs
        '''
        self.src_img = src_img
        self.args = args
        self.debug = debug
    
    def convert(self):
        '''
            @brief convert the source image to the images with line segments
        '''
        # from src_img to gray_scale_img
        gray_scale_img = cv.cvtColor(self.src_img, cv.COLOR_RGB2GRAY)
        if self.debug:
            cv.imshow(gray_scale_img)
        
        # from gray_scale_img to blur_img
        gaussian_kernal_size = (self.args.blur_radius, self.args.blur_radius)
        blur_img = cv.GaussianBlur(gray_scale_img, gaussian_kernal_size, 0)
        if self.debug:
            cv.imshow(blur_img)
        
        # use canny edge detection to dectect edges in blur_img
        canny_img = cv.Canny(blur_img,
                             self.args.canny_threshold_1,
                             self.args.canny_threshold_2,
                             apertureSize=self.args.aperture_size)
        if self.debug:
            cv.imshow(canny_img)
        
        # get line segments from canny_img
        line_segs = cv.HoughLinesP(canny_img, self.args.rho, self.args.theta,
                                   self.args.hough_threshold,
                                   minLineLength=self.args.min_line_length,
                                   maxLineGap=self.args.max_line_gap)
        
        # draw line segments to the result image
        seg_list = []
        res_img = np.zeros(self.src_img.shape, np.uint8)
        line_color = (0, 255, 0)
        if line_segs is not None:
            for i in range(0, len(line_segs)):
                l = line_segs[i][0]
                seg_list.append({
                    "start": (l[0], l[1]),
                    "end": (l[2], l[3])
                })
                cv.line(res_img, seg_list[i]["start"], seg_list[i]["end"],
                        line_color, 1, cv.LINE_AA)
        if self.debug:
            cv.imshow(res_img)
            print(seg_list)
        
        return seg_list
