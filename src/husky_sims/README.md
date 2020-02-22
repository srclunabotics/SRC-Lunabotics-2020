# Husky Sims Package

Package for simulating the clearpath Husky for testing of various algorithms.
The Husky is very similar in size and mass to our goal robot so it provides a good
platform for testing different types of control and possibly sensors.

Launch using roslaunch husky_sims arena_husky_bringup.launch

Required packages:
	Most are listed in here: http://wiki.ros.org/Robots/Husky

	ros-melodic-husky-simulator
	ros-melodic-husky-navigation
	ros-melodic-husky-gazebo
	ros-melodic-husky-viz

## TODO Gazebo Simulation

This package provides the necessary Gazebo configuration files for simulating a field that conforms to the NASA Lunabotics specifications. 
