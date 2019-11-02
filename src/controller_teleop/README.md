Package for controlling a simulated husky with a connected xbox one controller.
Use the left joystick to move forwards and backwards and the right joystick
to turn side to side.

Use the tutorial below to properly setup your joystick
http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick

Launch using roslaunch controller_teleop teleop_sim_husky.launch js:=<jsx where x is the joystick index matched with your connected controller>

Required packages:
	husky_sims

	Most husky packages are listed in here: http://wiki.ros.org/Robots/Husky

	ros-melodic-husky-simulator
	ros-melodic-husky-navigation
	ros-melodic-husky-gazebo
	ros-melodic-husky-viz
