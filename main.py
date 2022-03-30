import argparse
import subprocess

from ImageProcessing.paper import LETTER_PAPER
from ImageProcessing.image_processing import image_process
from InverseKinematics.convert import lines_to_instructions
from HardwareControl.controller import Controller

def main():
	# start pigpiod (pigpio daemon)
	subprocess.run(["sudo", "pigpiod"])
	
	# parse the command-line args
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--src_img_path",
						required=True, dest="src_img_path", action="store", type=str, help="Path to the source image")
	cmd_args = parser.parse_args()

	# start to process the image
	real_space_segments = image_process(cmd_args.src_img_path, LETTER_PAPER, False)
	instructions = lines_to_instructions(real_space_segments)
	controller = Controller()

	# start to draw the processed image
	try:
		controller.draw(instructions)
	except KeyboardInterrupt:
		print("Keyboard interrupt detected, releasing servos...")
		controller.clean_up()
		return

if __name__ == "__main__":
	main()
