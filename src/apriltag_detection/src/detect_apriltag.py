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

import argparse
from matplotlib import pyplot as plt
import apriltag
import apriltags3
# from skimage.color import rgb2gray
import time
import rospy
import math
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Global variable containing the location in the arena of the tags (x, z)
# IMNPORTANT: At the moment in the gazebo sim the axes don't math up with the axis of the 
# apriltag. Please refer to the table below to match axes between the world and the tag to
# get the correct locations of the tags
"""
    Apriltag axes       World axes
    x                   y
    y                   z
    z                   x

"""
# tag_locations = {
#                 3: (1.57, 3.92),
#                 8: (0.02, 2.02),
#                 15: (-1.47, 3.01)
#                 }

tag_locations = {
                10: (0, 0)                
                }


# Gets the direct distance from the camera to the april tag as well as the offset angle
def getAngleCorrection(x_cam, y_cam, z_cam, pose_R):
    """Calculates the correction angle the robot must assume to head towards the tag"""
    angle_correction_to_tag = math.degrees(math.atan2(x_cam, z_cam))
    return angle_correction_to_tag


def getThetas(pose_R):
    """Returns the angles between the tag and the camera.
    theta_x controls the height of the camera
    theta_y controls the left and right movement
    theta_z controls the tilt of the camera side to side"""
    theta_x = math.atan2(pose_R[2][1], pose_R[2][2])
    theta_y = math.atan2(-pose_R[2][0], math.sqrt( (pose_R[2][1])**2 + (pose_R[2][2])**2 ) )
    theta_z = math.atan2(pose_R[1][0], pose_R[0][0])
    return theta_x, theta_y, theta_z


def getRobotLocation(theta_x, theta_y, theta_z, distance, tag_locations, tag):
    """Uses eucledian distance between robot and tag, and angle theta_y to obtain the distance to the tag.
    Combine distance to tag with position of tag to obtain approx coordinates of robot's location."""
    tag_location_x, tag_location_z = tag_locations[int(tag.tag_id)]
    to_tag_z = distance * math.cos(theta_y)
    # print("to tag z" , to_tag_z)
    to_tag_x = distance * math.sin(theta_y)
    # print("to tag x", to_tag_x)

    # Get the estimated robot position based off its distance from the apriltags
    est_robot_x = tag_location_x + to_tag_x
    est_robot_z = tag_location_z + to_tag_z

    return est_robot_x, est_robot_z


def getDistances(x_cam, y_cam, z_cam):
    # Calculate first hypotenuse
    hypot1 = math.hypot(x_cam, z_cam)
    # Get the direct distance from the camera to the tag
    eucledian_distance = math.hypot(hypot1, y_cam)
    return eucledian_distance
    

# Function to detect any apiltags in a passed in image
def detectApriltag(ros_img):
    # Define the camera parameter that the detector needs
    # TODO: Find a better way to do this
    camera_parameters = [634.7421143901029, 638.4339498290706, 316.5133740410524, 217.848671299271] #[680.9565272862395, 678.9601430884998, 320.50156915761715, 233.43506067483017]

    # CvBridge object for converting image types
    bridge = CvBridge()

    # Convert from a ROS image to an OpenCv image that the detector can use
    cv_img = bridge.imgmsg_to_cv2(ros_img, 'bgr8')

    # path to apriltag image to load and detect
    # img = rgb2gray(frame) * 255
    # img = img.astype(np.uint8)
    img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # Get the size of the apriltag from the parameter server
    # TODO: Possibly move this outside so we aren't constantly pulling from the param server
    tag_size = rospy.get_param("/apriltag_detector/tag_size")

    # Get the list of tags from the detector
    tags = at_detector.detect(img, estimate_tag_pose=True, camera_params=camera_parameters, tag_size=tag_size)
    
    # In the future this will be replaced by a for each tag in tags loop to iterata through all the tags
    if tags == []:
        message = "\n\n no tag found"
    else:
        message = "\n\n"
        for tag in tags:
            x_cam = tag.pose_t[0]
            y_cam = tag.pose_t[1]
            z_cam = tag.pose_t[2]

            # Get the angle offset from the camera to the tag, and the correction to arrive at tag
            angle_correction_to_tag = getAngleCorrection(x_cam ,y_cam, z_cam, pose_R=tag.pose_R)
            distance = getDistances(x_cam, y_cam, z_cam)
            theta_x, theta_y, theta_z = getThetas(tag.pose_R)
            robot_x, robot_z = getRobotLocation(theta_x, theta_y, theta_z, distance, tag_locations, tag)
        
            theta_msg = "\n\ttheta_x = " + str(theta_x) + "\n\ttheta_y = " + str(theta_y) + "\n\ttheta_z = " + str(theta_z)

            path_msg = "\n\tDistance = " + str(tag.pose_t[2]) + " meters" + "\n\tAngle correction to tag = " + str(round(angle_correction_to_tag, 2))

            robot_location_msg = "\n\tRobot location est: " + "robot_x = " + str(round(robot_x, 3)) + " robot_z = " + str(round(robot_z,3))
            # message = message + str(tag.tag_id) + ":" + str(tag.pose_t) + "\n" + "RotMat = \n" + str(tag.pose_R) + "\n dot prod = \n" + str(test_translation) + "\n Distance = " + str(distance) + "\n" + "Angle = " + str(angle) + "\n\n"
            message = message + "\n\nTag ID = " + str(tag.tag_id) + ": " + theta_msg + path_msg + robot_location_msg
            
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

    # Get the image topic from the parameter server
    img_topic = rospy.get_param("/apriltag_detector/img_topic")

    # Subscriber that calls the detector callback function every time a new message is received on the topic 
    rospy.Subscriber(img_topic, Image, detectApriltag)

    rospy.spin()
    

            
