#! /usr/bin/env python3
import sys

try:
    from pymorse import Morse
except ImportError:
    print("Error: You need first to install pymorse, the Python bindings for Morse!")
    sys.exit(1)

def is_mouse_visible(semantic_cam_stream):
    """ Read data from the semantic camera, and determine if a specific object is within the field of view of the robot """
    data = semantic_cam_stream.get()
    visible_objects = data['visible_objects']
    for visible_object in visible_objects:
        if visible_object['name'] == "Mouse":
            return True
    
    return False


def main():
    """Use the semantic cameras to locate the target and follow it """
    with Morse() as simu:
    
        camL = simu.r2.camL
        camR = simu.r2.camR
        motion = simu.r2.motion2

        while True:
            seeing_at_left = is_mouse_visible(camL)
            seeing_at_right = is_mouse_visible(camR)

            if seeing_at_left and seeing_at_right: v_w = {"v":2, "w":0}    
            elif seeing_at_left: v_w = {"v":1.5, "w":1}
            elif seeing_at_right: v_w = {"v":1.5, "w":-1}
            else: v_w = {"v":0, "w":-1}

            motion.publish(v_w)

if __name__ == "__main__":
    main()
