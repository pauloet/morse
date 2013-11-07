#! /usr/bin/env python3.2
from pymorse import Morse
import math

def get_agent_position(pose_stream):
    """Read data from the pose sensor, and determine the agent position """
    pose = pose_stream.get()
    return pose



def main():
    minDist = 4.0   # Minimal distance to maintain between mouse and cat
    height = 2.5    # The height for the flying cat

    with Morse() as simu:

        while True:
            catPosition = get_agent_position(simu.r2.pose2)
            mousePosition = get_agent_position(simu.r1.pose1)

            if mousePosition and catPosition:
            # go behind the mouse
                waypoint = {    "x": mousePosition['x'] - minDist*math.cos(mousePosition['yaw']),\
                            "y": mousePosition['y'] - minDist*math.sin(mousePosition['yaw']),\
                            "z": height, \
                            "yaw": catPosition['yaw'], \
                            "tolerance": 0.5            
                    }

            # look at the mouse
            if mousePosition['x']==catPosition['x']:
                waypoint['yaw']=math.sign(mousePosition['y']-catPosition['y'])*math.pi
            else:
                waypoint['yaw']=math.atan2(mousePosition['y']-catPosition['y'], mousePosition['x']-catPosition['x'])

            # send command through the socket
            simu.r2.waypoint.publish(waypoint)


if __name__ == "__main__":
    main()

