#! /usr/bin/env python3
import sys

try:
    from pymorse import Morse
except ImportError:
    print("Error: You need first to install pymorse, the Python bindings for Morse!")
    sys.exit(1)

def pose_received(pose):
    print("The Robot is currently at %s" % pose)



print("Use WASD to control the robot 2")

with Morse() as simu:
    #print("here...")
    simu.r2.pose2.subscribe(pose_received)
    motion = simu.r2.motion2

    v=0.0
    w=0.0

    while True:
        key = input("WASD?")

        if key.lower() ==   "w": v += 0.1
        elif key.lower() == "s": v -= 0.1
        elif key.lower() == "a": w += 0.1
        elif key.lower() == "d": w -= 0.1
        else: continue

        motion.publish({"v":v, "w":w})
