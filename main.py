import os, sys

import cv2
import numpy as np


retval, corners = cv2.findChessboardCorners(image, patternSize, flags)


if __name__ == '__main__':

    args = sys.argv[1:]
    path = args[0]

# https://learnopencv.com/camera-calibration-using-opencv/