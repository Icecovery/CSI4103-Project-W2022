import math
import cv2 as cv;
import numpy as np;

# main function definition
def main():
	# Parameters

	p_BlurRadius = 21
	p_Threshold1 = 60
	p_Threshold2 = 10
	p_ApertureSize = 3
	p_Threshold3 = 8
	p_MinLineLength = 5
	p_MaxLineGap = 5
	p_Rho = 1
	p_Theta = np.pi / 180

	# ===================

	# read raw
	inputImg = cv.imread("input.png")
	cv.imshow("input raw", inputImg)

	#get image parameters
	height = inputImg.shape[0]
	width = inputImg.shape[1]

	# turn gray scale
	grayImg = cv.cvtColor(inputImg, cv.COLOR_RGB2GRAY)
	cv.imshow("gray scale", grayImg)

	# blur 
	if p_BlurRadius % 2 == 0:
		p_BlurRadius += 1 # blur radius must be odd
		print("p_BlurRadius must be odd!")
		
	blurImg = cv.GaussianBlur(grayImg, (p_BlurRadius, p_BlurRadius), 0)
	cv.imshow("blurred", blurImg)
	
	# canny edge detection
	if p_ApertureSize % 2 == 0:
		p_ApertureSize += 1  # aperture size must be odd
		print("p_ApertureSize must be odd!")
		
	cannyImg = cv.Canny(blurImg, p_Threshold1, p_Threshold2, apertureSize=p_ApertureSize)
	cv.imshow("canny edge", cannyImg)

	# trace lines
	lineSegments = cv.HoughLinesP(cannyImg, p_Rho, p_Theta, p_Threshold3, minLineLength=p_MinLineLength, maxLineGap=p_MaxLineGap)
	
	# create new blank image
	lineImg = np.zeros(inputImg.shape, np.uint8)
	
	# draw lines to image
	if lineSegments is not None:
		for i in range(0, len(lineSegments)):
			l = lineSegments[i][0]
			cv.line(lineImg, (l[0], l[1]), (l[2], l[3]), (0, 255, 0), 1, cv.LINE_AA)

	cv.imshow("lines", lineImg)

	# wait for key press to exit
	cv.waitKey()

# main program entry point
if __name__ == "__main__":
	main()