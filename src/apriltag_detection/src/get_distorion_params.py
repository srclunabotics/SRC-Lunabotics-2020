import numpy as np
import cv2
import glob

# Where to save and look for images
img_path = "../calibration_images/new_cam/"

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Kepp track of how many images we've saved
i = 0

print "Hold the calibration chessboard at different angles and rotations and hit s to save an image. Save at least 15 and hit q to generate parameters"

# Camera object for webcam. 
camera = cv2.VideoCapture(1) # If 1 doesn't work try 0

# image to be used for size later
ret, test_img = camera.read()

# convert to grayscale
test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

# Loop for saving calibation images
while(1):
	# Grab the frame
	ret, cv_img = camera.read()

	# Image to be saved because cv_img will be 
	save_img = cv_img.copy()

	# Convert to grayscale
	gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
	# cv2.imshow('img',cv_img)

	key = cv2.waitKey(1)

	# Find the chess board corners
	ret, corners = cv2.findChessboardCorners(gray_img, (9,6),None)

	# If found, add object points, image points (after refining them)
	if ret == True:
		corners2 = cv2.cornerSubPix(gray_img,corners,(11,11),(-1,-1),criteria)

		# Draw and display the corners
		corner_img = cv2.drawChessboardCorners(cv_img, (9,6), corners2,ret)
		cv2.imshow('img',corner_img)

		# Get key press
		key = cv2.waitKey(1)

		# Check if s was hit and sabve image if it was
		if key == ord('s'):
			cv2.imwrite(img_path + str(i) + '.jpg', save_img)
			i += 1

	# Check if q was hit and break out of the loop if it was
	if key == ord('q'):
		break

j = 1

# Get all .jpg files in the image path
images = glob.glob(img_path + '*.jpg')

num_imgs = len(images)

# Get camera parameters from saved images
for fname in images:
	img = cv2.imread(fname)	
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	# Find the chess board corners
	ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

	# If found, add object points, image points (after refining them)
	if ret == True:
		print "Collecting data from image " + str(j) + "/" + str(num_imgs)
		objpoints.append(objp)

		corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		imgpoints.append(corners2)

		# Draw and display the corners
		img = cv2.drawChessboardCorners(img, (9,6), corners2,ret)
		cv2.imshow('img',img)
		cv2.waitKey(100)
		j+=1

cv2.destroyAllWindows()

print "Calibrating...."

# Get the calibration matrix and store it in mtx
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, test_img.shape[::-1],None,None)

# Display the matrix 
print "Calibration matrix"
print mtx

print "Pastable format"
print str(mtx[0][0]) + ", " + str(mtx[1][1]) + ", " + str(mtx[0][2]) + ", " + str(mtx[1][2])
