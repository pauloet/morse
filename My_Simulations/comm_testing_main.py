#! /usr/bin/env python3.2
import sys
import communications_simulator as comm_simu

def main():

    r0r1 = comm_simu.Communication_Simulator('r00', 'r11')
    #r1r2.print_models()
    r0r1.set_model('abc')
    r1r2 = comm_simu.Communication_Simulator('r11', 'r22')
    r1r2.set_model('line_of_sight')
    print(r0r1.get_model())
    print(r1r2.get_model())
    r1r2.set_model('free_space_loss')
    print(r0r1.get_model())
    print(r1r2.get_model())

if __name__ == "__main__":
    main()
