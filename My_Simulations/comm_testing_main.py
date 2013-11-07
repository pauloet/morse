#! /usr/bin/env python3.2
import sys
import rcs
from time import sleep


def main():


    r1r2_1 = rcs.RCS('r1', 'r2', model = "distance")
    r1r2_2 = rcs.RCS('r1', 'r2', model = "line_of_sight")
    r1r2_3 = rcs.RCS('r1', 'r2', model = "free_space_loss", freq = 750)
    
    try:
        while True:
            print("Distance Model: %s" %(r1r2_1.can_communicate()))    
            print("Line of Sight Model: %s" %(r1r2_2.can_communicate()))
            print("Propagation Path Loss Model: %s" %(r1r2_3.can_communicate()))
            sleep(7)    # seconds
    except (KeyboardInterrupt, SystemExit):
        print(' --> Programm terminated.')
        raise     
    finally: 
        del r1r2_1
        del r1r2_2
        del r1r2_3
        pass

if __name__ == "__main__":
    main()
