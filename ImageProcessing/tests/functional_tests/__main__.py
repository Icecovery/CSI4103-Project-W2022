import argparse
import os
import cv2 as cv
import sys

# start: code to resolve relative imports
import sys
import importlib
from pathlib import Path

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

from ...paper import LETTER_PAPER
from ...image_processing import image_process

def export_path_csv(l):
	EXPORT_DIR = "Temp"
	EXPORT_FILE_NAME = "path.csv"
	FULL_EXPORT_FILE_PATH = os.path.join(EXPORT_DIR, EXPORT_FILE_NAME)

	# create temp folder
	if not os.path.exists(EXPORT_DIR):
		os.makedirs(EXPORT_DIR)

	with open(FULL_EXPORT_FILE_PATH, "w") as file:
		for i in range(len(l)):
			line = str(l[i][0][0]) + "," + str(l[i][0][1]) + "," + str(l[i][1][0]) + "," + str(l[i][1][1]) + "\n"
			file.write(line)

def main():
	# parse the command-line args
	parser = argparse.ArgumentParser()
	parser.add_argument("--debug",
						dest="debug", action="store_true", help="Enable debug outputs.")
	parser.add_argument("-s", "--src_img_path",
						required=True, dest="src_img_path", action="store", type=str, help="Path to the source image")
	parser.set_defaults(debug=False)
	cmd_args = parser.parse_args()

	real_space_segments = image_process(cmd_args.src_img_path, LETTER_PAPER, cmd_args.debug)

	export_path_csv(real_space_segments)

	if cmd_args.debug:
		# wait for key inputs to see the intermediate images
		cv.waitKey()

# main program entry point
if __name__ == "__main__":
	main()
