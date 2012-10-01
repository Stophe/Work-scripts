'''
Created on Sep 20, 2012

@author: chtho
'''
from vasp.find import Find
from os import listdir
from vasp.potcar import Potcar
from vasp.poscar import Poscar


def test_potcar():
    paths = Find(".", "POTCAR")
    for path in paths:
        potcar = Potcar(path).read_file()
        poscar = Poscar(path)
        if not len(potcar.potentials) == len(poscar.symbols):
            print "POTCAR not complete in %s" % path
            

if __name__ == '__main__':
    test_potcar()