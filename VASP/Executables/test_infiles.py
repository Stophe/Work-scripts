#!/usr/bin/env python
'''
Created on Sep 20, 2012

@author: chtho
'''

import os
from vasp.find import Find
from vasp.potcar import Potcar
from vasp.poscar import Poscar
from vasp.run import Run
from vasp.incar import Incar

def run_tests(starting_path):
    print "\nRunning tests\n" + 50*"-"
    paths = Find(starting_path, "RUN")
    if len(paths) != 0:
        if all_files_exist(paths):
            test_potcar(paths)
            test_run_file(paths)
            test_poscar(paths)
    else:
        print "No RUN files were found"
    print 50*"-" + "\nFinished tests\n"

def all_files_exist(paths):
    """
    Test to see that all files are present.
    """
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
    """
    Tests the potcar file and checks:
    - The same nr of atomic types in POTCAR as in POSCAR
    - The order in the POTCAR and POSCAR
    """
    for path in paths:
        potcar = Potcar(path, potentials=[]) #Can't figure out why the list needs to be reset...
        if os.path.isfile(os.path.join(path, 'POSCAR')):
            poscar = Poscar(path)
        else: # This will check NEB POSCARs that are presumed to be identical
            poscar = Poscar(os.path.join(path, '01'))
        if not len(potcar.potentials) == len(poscar.symbols):
            print "POTCAR not compatible in:\n%s" % path
            print "POSCAR: %s\tPOTCAR: %s" % (len(poscar.symbols), len(potcar.potentials))
        for i in range(0, len(poscar.symbols)):
            if poscar.symbols[i] in potcar.potentials[i]:
                pass
            else:
                print "Order or atoms in POTCAR is incorrect in:\n%s" % path
                print "POSCAR: %s\tPOTCAR: %s" % (' '.join(poscar.symbols),
                                                  ' '.join(potcar.potentials))
            
def test_run_file(paths):
    """
    Tests some run file stuff.
    Still a work in progress, the nodes npar check could should use cores instead of nodes.
    Need to think of a way to fix that.
    """
    for path in paths:
        run = Run(path)
        incar = Incar(path)
        if incar.npar != 4 and ( run.nodes % incar.npar > 0 or run.nodes == 0 or incar.npar == 0):
            print "Number of nodes and NPAR not compatible in:\n%s" % path
            print "Nodes: %s\tNPAR: %s" % (run.nodes, incar.npar)

def test_poscar(paths):
    """
    Completely useless test since Poscar only reads positions according to count.
    """
    for path in paths:
        if os.path.isfile(os.path.join(path, 'POSCAR')):
            poscar = Poscar(path)
        else:
            poscar = Poscar(os.path.join(path, '01'))
        if sum(poscar.counts) != len(poscar.supercell.atoms):
            print "Different nr of atomic positions than specified in:\n%s" % path
            print "Counts: %s\tPositions: %s" % (poscar.counts, len(poscar.supercell.atoms))
        
if __name__ == '__main__':
    print "\nRunning tests\n" + 50*"-"
    paths = Find(os.getcwd(), "RUN")
    if len(paths) != 0:
        if all_files_exist(paths):
            test_potcar(paths)
            test_run_file(paths)
            test_poscar(paths)
    else:
        print "No RUN files were found"
    print 50*"-" + "\nFinished tests\n"
