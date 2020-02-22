#!/usr/bin/env python

from tf import TransformBroadcaster
import rospy
from rospy import Time 
from gazebo_msgs.msg import ModelStates


def main():
    rospy.init_node('TF_broadcaster')

def tf_callback(msg):
    name = msg.name
    robot_index = name.index("/")
    pose = msg.pose[robot_index]
    
    b = TransformBroadcaster()
    
    rotation = (pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)
    
    translation = (pose.position.x, pose.position.y, pose.position.z)   
    b.sendTransform(translation, rotation, Time.now(), 'Our special Mining Bot', '/world')
    
# topic name: /gazebo/model_states
# message: ModelStates
if __name__ == '__main__':
    main()

    rospy.Subscriber('/gazebo/model_states', ModelStates, tf_callback)     
    rospy.spin()