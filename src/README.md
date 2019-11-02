# NASA Robotic Mining Competition: Lunabotics

The repository is organized into different ROS packages.

Steps for setup:
1. Clone the repository normally.
2. cd in the folder
3. Run catkin_make
4. Add the command "source /your_path/SeniorD-RMC-2019/devel/setup.bash" to your .bashrc file.
 	For example mine is /home/ryan/SeniorD-RMC-2019/devel/setup.bash
5. Run source ~/.bashrc to update your environment
6. Your environment should now be setup. Try to roscd into the different packages and roslaunch some of the packages after you've downloaded the necessary requirements

Please keep everything organized as ROS packages so you don't break other people's
catkin workspaces. Make branches and stuff obviously we'll talk about this later.

If any packages have a models folder you'll need to copy that into your /.gazebo/models directory in order for a world to spawn it.

Please try to include a README with any packages you make with their purpose and
the necessary packages to run them.
