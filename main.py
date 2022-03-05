from ImageProcessing.image_processing import image_process
from ImageProcessing.paper import Paper

# constants
SRC_IMG_PATH = "./ImageProcessing/tests/functional_tests/test_images/Test_image.jpeg"

# some paper pre-sets
LETTER_PAPER = Paper(279, 216, -50, 140)

def main():
    real_space_segments = image_process(SRC_IMG_PATH, LETTER_PAPER, False)
    print(real_space_segments)

if __name__ == "__main__":
    main()
