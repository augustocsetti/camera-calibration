import os
import sys
import pickle
from datetime import datetime

import cv2
import numpy as np
from tqdm import tqdm

CHECKERBOARD = (9,7)

# Arrays to store object points and image points from all the images
object_points = [] # 3D points in real world space
img_points = [] # 2D points in image plane

objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1],3), np.float32)
objp[:,:2] = np.mgrid[0:CHECKERBOARD[0],0:CHECKERBOARD[1]].T.reshape(-1,2) # x,y coordinates


def save_coefficients(mtx, dist, path) -> None:
    with open(f'{path}/coefficients.p', 'wb') as f:
        coef = {'mtx': mtx, 'dist': dist}
        pickle.dump(coef, f)

def load_coefficients(path) -> tuple:
    '''Reads the coefficients from a path and return it.\n
    - Return: tuple(mtx, dist)'''

    with open(f'{path}/coefficients.p', 'rb') as f:
        coef = pickle.load(f)
    return coef['mtx'], coef['dist']

def main(path: str, correct_files: bool = True):
    '''
    Function that receives a image file path to calibrate the camera that took the pictures.\n
    The function also store the parameters and save the corrected images on results directory.
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
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # detecting boards on chessboard
        retval, corners = cv2.findChessboardCorners(image=img, patternSize=CHECKERBOARD, flags=None)
        # cv2.drawChessboardCorners(img, (7, 9), corners, retval)
        
        # if borders were detected
        if retval:
            # refine detected boards
            # corners2 = cv2.cornerSubPix(image, corners, winSize, zeroZone, criteria)

            #
            img_points.append(corners)
            object_points.append(objp)  


    # calibrate
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, img_points, img.shape[::-1], None, None)
    # print(ret, mtx, dist, rvecs, tvecs)

    # creating the results path
    os.makedirs(f'results', exist_ok=True)
    date = datetime.now().strftime('%d-%m-%Y %H-%M')
    destinyPath = path.split('\\')[-2]+date
    os.makedirs(f'results/{destinyPath}')

    # saving cefficients
    save_coefficients(mtx, dist, f'results/{destinyPath}')

    # correcting images
    if correct_files:
        print('\nUndistort images...')
        for image in tqdm(images):
            img = cv2.imread(f'{path}{image}')
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, img_points, img.shape[1:], None, None)
            img_undistort = cv2.undistort(img, mtx, dist, None, mtx)
            cv2.imwrite(f'./results/{destinyPath}/{image}', img_undistort)


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
