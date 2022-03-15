import argparse

from ImageProcessing.paper import LETTER_PAPER
from ImageProcessing.image_processing import image_process
from InverseKinematics.convert import lines_to_angles
from HardwareControl.controller import Controller

def main():
	# parse the command-line args
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--src_img_path",
						required=True, dest="src_img_path", action="store", type=str, help="Path to the source image")
	cmd_args = parser.parse_args()

	real_space_segments = image_process(cmd_args.src_img_path, LETTER_PAPER, False)
	angle_sets = lines_to_angles(real_space_segments)
	controller = Controller()
	try:
		controller.draw(angle_sets)
	except KeyboardInterrupt:
		print("Keyboard interrupt detected, releasing servos...")
		controller.clean_up()
		return

if __name__ == "__main__":
	main()
