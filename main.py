import os
import sys
from datetime import datetime

import cv2
import numpy as np
from tqdm import tqdm

from handle_data import *


# chessboard size
CHECKERBOARD = (9,7)

# set criteria to refine the detection of subpix of a boarder (more on README.md -> References)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Arrays to store object points and image points from all the images
object_points = [] # 3D points in real world space
img_points = [] # 2D points in image plane

# build vector to store object points
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1],3), np.float32)
objp[:,:2] = np.mgrid[0:CHECKERBOARD[0],0:CHECKERBOARD[1]].T.reshape(-1,2) # x,y coordinates


def main(path: str, correct_files: bool = True):
    '''
    Function that receives a image file path, calibrate the camera,\n
    store the coefficients and save the undistort images.
    '''

    # getting image file names
    images = os.listdir(path)
    print(f'Directory: {path}')
    print('Images:')
    for i in images:
        print(f'\t{i}')
    print('\n')

    # processing images
    print('Getting coefficients...')
    for image in tqdm(images):
        
        # openning a image 
        img = cv2.imread(f'{path}{image}')
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to gray

        # detecting boards on chessboard
        retval, corners = cv2.findChessboardCorners(img_gray, CHECKERBOARD, None)
        
        # if borders were detected
        if retval:
            # refine detected boards
            corners2 = cv2.cornerSubPix(img_gray, corners, (11, 11), (-1,-1), criteria)

            # add to image and object points
            img_points.append(corners2)
            object_points.append(objp)

        # show board detection
        # img_detected = cv2.drawChessboardCorners(img, (7, 9), corners2, retval)
        # img_detected = cv2.resize(img_detected, (int(1920/3), int(2560/3)))
        # cv2.namedWindow('detected board', cv2.WINDOW_NORMAL) 
        # cv2.imshow('detected board', img_detected)
        # cv2.waitKey(0)

    # calibrate camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, img_points, img_gray.shape[::-1], None, None)
    print(f'\n- intrinsic parameters')
    print(f'\tmtx:\n{mtx}')
    print(f'\tdist:\n{dist}')

    # getting error
    mean_error = 0
    for i in range(len(object_points)):
        imgpoints2, _ = cv2.projectPoints(object_points[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(img_points[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    error = mean_error/len(object_points)
    print(f'\n- total error: {error}')

    # creating the results path
    os.makedirs(f'results', exist_ok=True)
    date = datetime.now().strftime('%d-%m-%Y %H-%M')
    destinyPath = path.split('\\')[-2]+date
    os.makedirs(f'results/{destinyPath}')

    # saving coefficients
    save_coefficients(mtx, dist, f'results/{destinyPath}')

    # correcting images
    if correct_files:
        print('\nUndistort images...')
        for image in tqdm(images):
            img = cv2.imread(f'{path}{image}')

            # getting new camera matrix (to auto crop with alpha = 0)
            h,  w = img.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))      

            # undistort and save img
            img_undistort = cv2.undistort(img, mtx, dist, None, newcameramtx)
            cv2.imwrite(f'./results/{destinyPath}/{image}', img_undistort)
            
    print('\nDone!')


if __name__ == '__main__':

    print('------------------------ Camera Calibration ------------------------\n')

    args = sys.argv[1:]
    
    if args:
        path = args[0]
        if path[-1] != '\\':
            path += '\\'

        main(path)

    else:
        print('Error! Please insert an image path as parameter.')
