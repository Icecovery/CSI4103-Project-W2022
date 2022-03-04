#!/bin/sh

PAPER_HEIGHT=279
PAPER_WIDTH=216
X_OFFSET=-50
Y_OFFSET=140
ARM_A_LENGTH=160
ARM_B_LENGTH=150
A_OFFSET=38.69
B_OFFSET=0.0

IMAGE_PATH="ImageProcessing/test_images/Test_image.jpeg" 

python3 ImageProcessing -s IMAGE_PATH --height $PAPER_HEIGHT --width $PAPER_WIDTH -x $X_OFFSET -y $Y_OFFSET --debug
# python3 InverseKinematics -la $ARM_A_LENGTH -lb $ARM_B_LENGTH --offset_a $A_OFFSET --offset_b $B_OFFSET -s "Temp/path.csv" --debug