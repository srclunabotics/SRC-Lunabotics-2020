# from __future__ import print_function
#!usr/bin/env python
import sys
import os
import cv2
import numpy as np
path_to_library = 'apriltags3-py' #Paste here the path to apriltags3-py you cloned
sys.path.insert(1, path_to_library)
import cv2
import argparse
from matplotlib import pyplot as plt
import apriltag
import apriltags3
# from skimage.color import rgb2gray
import time
import rospy
from sensor_msgs.msg import Image
import cv_bridge

def detect_apriltag(frame, camera_parameters):

    # path to apriltag image to load and detect
    # img = rgb2gray(frame) * 255
    # img = img.astype(np.uint8)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    tags = at_detector.detect(img, estimate_tag_pose=True, camera_params=camera_parameters, tag_size=0.172)
    
    if tags == []:
        message = "\n\n no tag found"
    elif len(tags) == 1:
        message = "\n\n" + str(tags[0].tag_id) + "\n" + str(tags[0].pose_t)
    elif len(tags) == 2:
        message = "\n\n" + str(tags[0].tag_id) + "|" + str(tags[0].pose_t) + "\n" + str(tags[1].tag_id) + "|" + str(tags[1].pose_t)
    
    return message


if __name__ == "__main__":
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    camera_parameters = [680.9565272862395, 678.9601430884998, 320.50156915761715, 233.43506067483017]

        # Detector parameters explained in https://github.com/duckietown/apriltags3-py
    at_detector = apriltags3.Detector(searchpath=[str(path_to_library)+'/apriltags/lib'], 
                           families='tag36h11',
                           nthreads=1,
                           quad_decimate=1.0,
                           quad_sigma=0.0,
                           refine_edges=1,
                           decode_sharpening=0.25,
                           debug=0)

    i=0
    while True:
        check, frame = webcam.read()
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        tags = detect_apriltag(frame, camera_parameters)   
        print(tags)
        # time.sleep(1)

        
        if key == ord('s'): 
            cv2.imwrite(filename='calibration_images/webcam/new_images/saved_img.jpg', img=frame)
            webcam.release()

            cv2.destroyAllWindows()

            print("Image saved!")
            break
            
        
        elif key == ord('q'):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

            
