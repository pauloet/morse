#! /usr/bin/env python3.2
from pymorse import Morse
import sys

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
        q = 'q'
        a = 'a'
        b = 'b'
        c = 'c'
        while True:
                print('\n***** Communications Simulator *****\nOptions:\n\t1st case (a) -> Distance factor \n\t2nd case (b) -> Line of Sight')
                print('\t3rd case (c) -> Loss(dB) Propagation Model\n\tExit the program (q)')
                option = str(input("Choice: "))
                if option == q: sys.exit(0)
                elif option == a: permission_2_communicate(1, 'r1', 'r2')
                elif option == b: permission_2_communicate(2, 'r1', 'r2')
                elif option == c: permission_2_communicate(3, 'r1', 'r2')
                else: sys.stderr.write("\nOups! Bad input. Try again.")

if __name__ == "__main__":
    main()
