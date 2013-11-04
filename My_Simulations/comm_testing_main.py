#! /usr/bin/env python3.2
import sys
import communications_simulator as comm_simu

def main():

    r0r1 = comm_simu.Communication_Simulator('r00', 'r11')
    r0r1.set_model('abc')
    r1r2 = comm_simu.Communication_Simulator('r11', 'r22')
    r1r2.set_model('line_of_sight')


    r2r3 = comm_simu.Communication_Simulator('r22', 'r33', model = "empiric_1")
    print(r2r3.get_model())
    r2r3.set_model('line_of_sight')
    print(r2r3.get_model())
    r2r3 = comm_simu.Communication_Simulator('r22', 'r33')
    print(r2r3.get_model())
    r2r3 = comm_simu.Communication_Simulator('r22', 'r33', model = "non_existance")
    print(r2r3.get_model())
    
    r2r3 = comm_simu.Communication_Simulator('r22', 'r33', mod = "non_existance")
    print(r2r3.get_model())

if __name__ == "__main__":
    main()
