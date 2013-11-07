#! /usr/bin/env morseexec
from morse.builder import *
import logging




# Append ATRV robot to the scene
robot = ATRV()
robot.name = "Paulo"

# Append an actuator
motion = MotionVW()
motion.translate(x=.2, z=1)
robot.append(motion)

# Append a sensor
pose = Pose()
pose.translate(z = 0.75)
robot.append(pose)

# Configure the robot on the 'socket' interface
robot.add_default_interface('socket')

env = Environment('indoors-1/indoor-1')


logger = logging.getLogger("morse." + __name__)
logger.info("info")
logger.debug("debug")
