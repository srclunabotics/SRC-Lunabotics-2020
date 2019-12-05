#!/usr/bin/env python
# from __future__ import print_function
import sys
import os
import cv2
import numpy as np

# Get the current directory of the file
dir_path = os.path.dirname(os.path.realpath(__file__))
# Remove the src from the end so we're in the directory above
dir_path = dir_path[:-3]

# Create the path to the library 
path_to_library = dir_path + 'apriltags3-py' #Paste here the path to apriltags3-py you cloned
# Add the path to the system path so the interpreter can find the library
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
from cv_bridge import CvBridge, CvBridgeError

def detect_apriltag(ros_img):
    # Define the camera parameter that the detector needs
    # TODO: Find a better way to do this
    camera_parameters = [680.9565272862395, 678.9601430884998, 320.50156915761715, 233.43506067483017]

    # CvBridge object for converting image types
    bridge = CvBridge()

    # Convert from a ROS image to an OpenCv image that the detector can use
    cv_img = bridge.imgmsg_to_cv2(ros_img, 'bgr8')

    # path to apriltag image to load and detect
    # img = rgb2gray(frame) * 255
    # img = img.astype(np.uint8)
    img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # Get the list of tags from the detector
    tags = at_detector.detect(img, estimate_tag_pose=True, camera_params=camera_parameters, tag_size=0.172)
    
    # In the future this will be replaced by a for each tag in tags loop to iterata through all the tags
    if tags == []:
        message = "\n\n no tag found"
    elif len(tags) == 1:
        message = "\n\n" + str(tags[0].tag_id) + "\n" + str(tags[0].pose_t)
    elif len(tags) == 2:
        message = "\n\n" + str(tags[0].tag_id) + "|" + str(tags[0].pose_t) + "\n" + str(tags[1].tag_id) + "|" + str(tags[1].pose_t)
    
    print message


if __name__ == "__main__":
    # Initialize the node
    rospy.init_node('apriltag_detector', anonymous=True)

    # Apriltag detector object imported from the external library
    at_detector = apriltags3.Detector(searchpath=[str(path_to_library)+'/apriltags/lib'], 
                           families='tag36h11',
                           nthreads=1,
                           quad_decimate=1.0,
                           quad_sigma=0.0,
                           refine_edges=1,
                           decode_sharpening=0.25,
                           debug=0)

    # Subscriber that calls the detector callback function every time a new message is received on the topic 
    rospy.Subscriber("camera_img", Image, detect_apriltag)

    rospy.spin()
    
    
    
    # key = cv2.waitKey(1)
    # webcam = cv2.VideoCapture(0)
    # camera_parameters = [680.9565272862395, 678.9601430884998, 320.50156915761715, 233.43506067483017]

    #     # Detector parameters explained in https://github.com/duckietown/apriltags3-py
    # at_detector = apriltags3.Detector(searchpath=[str(path_to_library)+'/apriltags/lib'], 
    #                        families='tag36h11',
    #                        nthreads=1,
    #                        quad_decimate=1.0,
    #                        quad_sigma=0.0,
    #                        refine_edges=1,
    #                        decode_sharpening=0.25,
    #                        debug=0)

    # i=0
    # while True:
    #     check, frame = webcam.read()
    #     cv2.imshow("Capturing", frame)
    #     key = cv2.waitKey(1)
    #     detect_apriltag(frame, camera_parameters)   
    #     # print(tags)
    #     # time.sleep(1)

        
    #     if key == ord('s'): 
    #         cv2.imwrite(filename='calibration_images/webcam/new_images/saved_img.jpg', img=frame)
    #         webcam.release()

    #         cv2.destroyAllWindows()

    #         print("Image saved!")
    #         break
            
        
    #     elif key == ord('q'):
    #         print("Turning off camera.")
    #         webcam.release()
    #         print("Camera off.")
    #         print("Program ended.")
    #         cv2.destroyAllWindows()
    #         break

            
