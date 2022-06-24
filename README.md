# Camera Calibration App

## Description
Camera calibration using OpenCV with Python. This simple application reads a file path with distorted pictures and stores the undistorted files and the coefficients founded for the camera.

## Installation
Use the package manager pip to install the requirements file.<br>
```pip install -r requirements.txt```

## Usage
The application receives a file path and, when executed, it prints the intrinsic parameters and the error. When finished the script stores corrected images and the coefficients (in pickle format) in the results folder.<br>
To run the application use the command bellow.<br>
```python main.py <imagePath>```<br><br>
Example:<br>
```python main.py .\photos\06-06-2022```

## References
- https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
- https://learnopencv.com/camera-calibration-using-opencv/
- https://medium.com/analytics-vidhya/camera-calibration-with-opencv-f324679c6eb7
- https://aliyasineser.medium.com/opencv-camera-calibration-e9a48bdd1844
- https://stackoverflow.com/questions/18955760/how-does-cvtermcriteria-work-in-opencv

## To do
- Split main function
- Improve parameters insertion
- Implement: read the coefficients files and undistor a entry path image