from ImageProcessing.paper import Paper
from ImageProcessing.image_processing import image_process
from InverseKinematics.convert import lines_to_angles
from HardwareControl.controller import Controller

# constants
SRC_IMG_PATH = "./ImageProcessing/tests/functional_tests/test_images/Test_image.jpeg"

# some paper pre-sets
LETTER_PAPER = Paper(279, 216, -50, 140)

def main():
	real_space_segments = image_process(SRC_IMG_PATH, LETTER_PAPER, False)
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
