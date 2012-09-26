#!/usr/bin/env python
'''
Created on Sep 20, 2012

@author: chtho
'''
from vasp.find import Find
import os
from vasp.potcar import Potcar
from vasp.poscar import Poscar

def all_files_exist(paths):
    all_here = True
    for path in paths:
        list_of_files_in_path = os.listdir(path)
        if 'POSCAR' not in list_of_files_in_path:
            #If the calculation is a NEB the 01 sub-folder is also checked
            if not os.path.isfile(os.path.join(path, '01', 'POSCAR')):
                print "No POSCAR file present in:\n%s" % path
                all_here = False
        elif 'POTCAR' not in list_of_files_in_path:
            print "No POTCAR file present in:\n%s" % path
            all_here = False
        elif 'INCAR' not in list_of_files_in_path:
            print "No INCAR file present in:\n%s" % path
            all_here = False
        elif 'KPOINTS' not in list_of_files_in_path:
            print "No KPOINTS file present in:\n%s" % path
            all_here = False
    return all_here
        


def test_potcar(paths):
    for path in paths:
        potcar = Potcar(path).read_file()
        if os.path.isfile(os.path.join(path, 'POSCAR')):
            poscar = Poscar(path)
        else: # This will check NEB POSCARs that are presumed to be identical
            poscar = Poscar(os.path.join(path, '01', 'POSCAR'))
        if not len(potcar.potentials) == len(poscar.symbols):
            print "POTCAR not complete in:\n%s" % path
        for i in range(0, poscar.symbols):
            if poscar.symbol[i] != potcar.potential[i]:
                print "Order or atoms in POTCAR is incorrect in:\n%s" % path
            

if __name__ == '__main__':
    paths = Find(".", "RUN")
    if len(paths) != 0:
        if all_files_exist(paths):
            test_potcar(paths)
    else:
        print "No RUN files were found"

