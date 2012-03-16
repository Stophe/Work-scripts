#!/usr/bin/env python

from vasp.supercell import SuperCell
from vasp.atom import Atom
from numpy import array
from vasp.primitive_cell import PrimitiveCell


def main():

    # Set up basis and primitive cell
    print '\nSetting up cell...\n'
    a0 = 4.2557
    ti1 = Atom('Ti', array([0., 0., 0.]))
    n1 = Atom('N', array([0.5, 0.5, 0.]))
    ti2 = Atom('Ti', array([0.5, 0.5, 0.5]))
    n2 = Atom('N', array([0., 0., 0.5]))
    primitive_cell = PrimitiveCell(array([0.5, 0.5, 0.]),
                                   array([-0.5, 0.5, 0.]),
                                   array([0., 0., 1]))
    supercell = SuperCell(a0, primitive_cell, [ti1, ti2, n1, n2])

    # Expand the cell
    add = (1, 1, 2)
    print ("Expanding cell %i, %i and %i times in a1, a2 and a3 direction...\n"
           % (add[0], add[1], add[2]))
    supercell.expand_3D(add)

    # Stop the lowest half of the atoms from relaxing
    for atom in supercell.atoms:
        if atom.position[2] < supercell.get_highest_position(2) / 2.:
            atom.relaxation = ['F', 'F', 'F']

    # Add vacuum
    print "Adding vacuum...\n"
    vacuum = 25  # Angstrom
    supercell.add_vacuum(vacuum)

    # Remove one layer to get a mirror symmetric structure
    print "Removing side layers...\n"
    supercell.remove_layer(supercell.get_highest_position(2))

    # Change a top layer atom
    supercell.convert_atom_on_surface('Ti', 'Al')

    # Print to POSCAR
    print "Save in POSCAR...\n"
    title = supercell.atom_counts('title')
    # Path to save the POSCAR in
    path = '/Users/chtho/Dropbox/Shared/TiN/001/'
    supercell.save_structure(path, title, 'poscar', relaxation=True)


if __name__ == '__main__':
    main()
