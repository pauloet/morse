from morse.builder import *

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

controller1 = Keyboard()
r1.append(controller1)


""" Building the 2nd Robot 'r2' """
r2 = B21()
r2.translate(x=-5)       # Start with a jump and away from r1
motion2 = MotionVW()     # Create a new instance of the actuator
motion2.translate(z=0.3) # Place the component at the specific location (x,y,z)
pose2 = Pose()           # Create a new instance of the sensor
pose2.translate(z=0.83)  # Place de component at the specific location (x,y,z)
r2.append(motion2); r2.append(pose2);
r2.add_default_interface('socket')

""" Choosing an Environment """
env = Environment('indoors-1/boxes')
env.place_camera([5, -5, 6])
env.aim_camera([1.0470, 0, 0.7854])
