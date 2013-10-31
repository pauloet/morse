#! /usr/bin/env python3.2
from pymorse import Morse
import sys
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

def permission_2_communicate(judgment, r1, r2):
    try:
        with Morse() as morse:
            results = morse.rpc('communication', 'distance_and_view', r1, r2)
            
            if judgment == 1:   # Only Distance Factor (assuming a circle around each robot with a maximum radius)
                maximum_radius = 5; # meters (or blender units)
                if results[0] <= maximum_radius: print('YES')
                else:   print('NO')
            elif judgment == 2: # Only based in the Sight of View
                if results[1] == True:  print('YES')
                else:   print('NO')
            else:
                print('Case not implemented yet...')


    except pymorse.MorseServerError as mse:
        print('Oups! An error occurred!')
        print(mse)

                
def main():
        while True:
                print('\n***** Communications Simulator *****\nOptions:\n\t1st case (1) -> Distance factor \n\t2nd case (2) -> Line of Sight')
                print('\t3rd case (3) -> Loss(dB) Propagation Model\n\tExit the program (0)')
                option = int(input("Choice: "))
                if option == 0: sys.exit(0)
                elif option == 1: permission_2_communicate(option, 'r1', 'r2')
                elif option == 2: permission_2_communicate(option, 'r1', 'r2')
                elif option == 3: permission_2_communicate(option, 'r1', 'r2')
                else: sys.stderr.write("\nOups! Bad input. Try again.")

if __name__ == "__main__":
    main()
