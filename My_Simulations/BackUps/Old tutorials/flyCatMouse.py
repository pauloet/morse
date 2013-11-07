#! /usr/bin/env morseexec
# Mark then your script as executable (chmod + file.py), and run as ./file.py
import logging
from morse.builder import *
from math import pi
logging.basicConfig(filename = "robots_communications.log")#, level = logging.DEBUG)
logger = logging.getLogger("morse.robots_communications" + __name__)

""" Building the 1st Robot 'r1' """
r1 = ATRV()
r1.translate(x=-1, z=1)       # Start with a jump :)
motion1 = MotionVW()     # Create a new instance of the actuator
motion1.translate(z=0.3) # Place the component at the specific location (x,y,z)
pose1 = Pose()           # Create a new instance of the sensor
pose1.translate(z=0.83)  # Place de component at the specific location (x,y,z)
r1.append(motion1); r1.append(pose1);     # Appending Actuator and Sensor to 'r1'
# Configuring the middlewares of ALL the robot components: Data-streams & Services
r1.add_default_interface('socket')
r1.properties(Object = True, Graspable = False, Label = "Mouse")
controller1 = Keyboard()
controller1.properties(Speed = 4.0)
r1.append(controller1)


""" Building the 2nd Robot 'r2' """
r2 = Quadrotor()
r2.translate(x=-5, z=1);      r2.rotate(z=pi/3);       
pose2 = Pose()           # Create a new instance of the sensor
pose2.translate(z=0.1)  # Place de component at the specific location (x,y,z)
r2.append(pose2);
cam = SemanticCamera()
cam.translate(x=0.3, z=-0.05); cam.rotate(x=0.2); cam.properties(Vertical_Flip=False);
r2.append(cam);
waypoint = RotorcraftWaypoint()
r2.append(waypoint)
r2.add_default_interface('socket')

""" Choosing an Environment """
env = Environment('indoors-1/boxes')
env.place_camera([5, -5, 6])
env.aim_camera([1.0470, 0, 0.7854])
env.select_display_camera(cam)


logger.debug("********** DEBUG MSG **********")
logger.info('********** INFO MSG **********')
