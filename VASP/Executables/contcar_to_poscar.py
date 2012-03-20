#!/usr/bin/env python
'''
Created on Mar 20, 2012

@author: chtho
'''
from os import getcwd

from vasp.contcar import Contcar
from vasp.find import Find


def main():
    starting_path = getcwd()
    found = Find(starting_path, 'CONTCAR')

    for path in found.paths:
        contcar = Contcar(path)
        contcar.supercell.convert_atom_on_surface('Al', 'Ti')
        title = "TiN(110) 2x2x%i" % (contcar.formula_unit / 4)
        contcar.supercell.save_structure(path, title, file_type='POSCAR',
                                         relaxation=True)

if __name__ == '__main__':
    main()
