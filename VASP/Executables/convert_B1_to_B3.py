'''
Created on Oct 20, 2014

@author: chtho
'''
from vasp.poscar import Poscar
from os import getcwd

def convert_structure():
    poscar = Poscar(getcwd())
    poscar.title = 'Converted from B1 to B3'
    sc = poscar.supercell
    
    supercell_x = int(raw_input("Supercells in x-direction: "))
    supercell_y = int(raw_input("Supercells in y-direction: "))
    supercell_z = int(raw_input("Supercells in z-direction: "))
    
    for atom in sc.atoms:
        if atom.symbol == 'N':
            atom.position[0] = atom.position[0] - 0.25/supercell_x
            atom.position[1] = atom.position[1] - 0.25/supercell_y
            atom.position[2] = atom.position[2] - 0.25/supercell_z
    
    poscar.create_file()


if __name__ == '__main__':
    print "\n\tConverting Poscar from B1 to B3\n"
    convert_structure()
