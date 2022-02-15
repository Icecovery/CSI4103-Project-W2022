import argparse
import cv2 as cv
import numpy as np
import os
import image_converter

# main program entry point
if __name__ == "__main__":
	# parse the command-line args
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", dest="debug", action="store_true", help="Enable debug outputs.")
	parser.set_defaults(debug=False)
	parser.add_argument("--src_img_path", required=True, dest="src_img_path", action="store", type=str, help="Path to the source image")
	cmd_args = parser.parse_args()
	
	# read the source image
	src_img = cv.imread(cmd_args.src_img_path)
	image_converter_args = ImageConverterArgs(
		blur_radius=21,
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
	image_converter = ImageConverter(src_img, image_converter_args, cmd_args.debug)
	image_converter.convert()

	if cmd_args.debug:
		cv.waitKey()
    
  
	# export line coordinates
	#if (input("Export path? (y/n): ").lower() == "y"):
	#	ExportPath(lineSegments)

  def ExportPath(lineSegments):
	  # create temp folder
	  if not os.path.exists('../Temp'):
		  os.makedirs('../Temp')

	  # write lines
	  file = open("../Temp/path.csv", "w")
	  for i in range(len(lineSegments)):
		  l = lineSegments[i][0]
		  file.write(str(l[0]) + "," + str(l[1]) + "," + str(l[2]) + "," + str(l[3]) + "\n")

    file.close()
