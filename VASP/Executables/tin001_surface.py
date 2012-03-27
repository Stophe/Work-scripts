#!/usr/bin/env python
from os import makedirs

from vasp.supercell import SuperCell
from vasp.atom import Atom
from numpy import array
from vasp.primitive_cell import PrimitiveCell


def main():

    supercell_width = 3
    supercell_depth = 3

    starting_path = ('/Users/chtho/Dropbox/Shared/TiN/001/Layer_test/%ix%ixL' %
                     (supercell_width, supercell_depth))
    try:
        makedirs(starting_path)
    except:
        print "%s already exists" % starting_path

    for i in range(1, 4):

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
        supercell_half_layer = supercell.copy()

        # Expand the cell
        add = (supercell_width - 1, supercell_depth - 1, i)
        print ("Expanding cell %i, %i and %i times in a1, a2 and a3 direction...\n"
               % (add[0], add[1], add[2]))
        supercell.expand_3D(add)
        supercell_half_layer.expand_3D(add)

        # Remove one layer to get a mirror symmetric structure
        print "Removing top layer...\n"
        supercell_half_layer.remove_layer(supercell_half_layer.get_highest_position(2))

        # Stop the lowest half of the atoms from relaxing
        for atom in supercell.atoms:
            if atom.position[2] < supercell.get_highest_position(2) / 2.:
                atom.relaxation = ['F', 'F', 'F']

        for atom in supercell_half_layer.atoms:
            if atom.position[2] < supercell_half_layer.get_highest_position(2) / 2.:
                atom.relaxation = ['F', 'F', 'F']

        # Add vacuum
        print "Adding vacuum...\n"
        vacuum = 25  # Angstrom
        supercell.add_vacuum(vacuum)
        supercell_half_layer.add_vacuum(vacuum)

        # Change a top layer atom
        #supercell.convert_atom_on_surface('Ti', 'Al')
        #supercell_half_layer.convert_atom_on_surface('Ti', 'Al')

        # Print to POSCAR
        print "Save in POSCAR...\n"
        title = (supercell.atom_counts('title') + " %ix%ix%i" %
                 (supercell_width, supercell_depth, i + 1))
        path = (starting_path + "/%ix%ix%i/" %
                (supercell_width, supercell_depth, i + 1))
        title_hl = (supercell_half_layer.atom_counts('title') + "%ix%ix%i.5" %
                    (supercell_width, supercell_depth, i))
        path_hl = (starting_path + "/%ix%ix%i.5" %
                   (supercell_width, supercell_depth, i))
        try:
            makedirs(path)
        except:
            print"%s already exists" % path
        try:
            makedirs(path_hl)
        except:
            print"%s already exists" % path

        supercell.save_structure(path, title, 'poscar', relaxation=True)
        supercell_half_layer.save_structure(path_hl, title_hl,
                                            'poscar', relaxation=True)


if __name__ == '__main__':
    main()
