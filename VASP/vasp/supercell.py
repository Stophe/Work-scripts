#!/usr/bin/env python

from numpy import array
from numpy import dot
from numpy.linalg import norm
from datetime import datetime
from copy import deepcopy
from vasp.atom import Atom
from vasp.primitive_cell import PrimitiveCell


class SuperCell:

    def __init__(self, a0, pc, list_of_atoms):
        """
        SuperCell is initiated with a lattice parameter, primitive cell and
        a list of atoms for the basis.
        """
        self.a0 = a0
        self.primitive_cell = pc
        self.atoms = []
        for atom in list_of_atoms:
            self.atoms.append(atom)

    def __repr__(self):
        return self.atoms

    def add(self, symbol, position):
        self.atoms.append(Atom(symbol, position))

    def expand_3D(self, times):
        """
        Input how many times in each direction the structure should be
        repeated.

        Ex: expand_3D((1,2,0))
        """
        self.expand_1D(times[0], 0)
        self.expand_1D(times[1], 1)
        self.expand_1D(times[2], 2)

    def expand_1D(self, times, direction=2):
        if times != 0:
            temp_atoms = []
            for atom in self.atoms:
                for i in range(1, times + 1):
                    temp_atoms.append(deepcopy(atom))
                    temp_atoms[-1].position[direction] = (
                        temp_atoms[-1].position[direction] + i)
            self.atoms = self.atoms + temp_atoms
            self.primitive_cell.matrix[direction] = (
                self.primitive_cell.matrix[direction] * (times + 1))
            for atom in self.atoms:
                atom.position[direction] = (atom.position[direction] /
                                            (times + 1))
            self.sort()
        else:
            pass

    def sort(self):
        new_list = sorted(self.atoms, key=lambda atom: atom.symbol,
                          reverse=True)
        self.atoms = new_list

    def convert_atom_on_surface(self,from_symbol, to_symbol):
        for atom in self.atoms:
            if (atom.symbol == from_symbol and 
                atom.position[2] == self.get_highest_position(2)):
                atom.symbol = to_symbol
                break
        self.sort()

    def add_vacuum(self, vacuum, direction=2): 
        # Adds vacuum layer given in Angstrom		
        norm_a_real = self.a0 * norm(self.primitive_cell.matrix[direction])
        displacement_factor = (vacuum - (1 - self.get_highest_position()) * norm_a_real) / norm_a_real + 1

        for atom in self.atoms:
            atom.position[direction] = atom.position[direction] / displacement_factor

        self.primitive_cell.matrix[direction] = self.primitive_cell.matrix[direction] * displacement_factor

    def atom_counts(self, only):
        types = []
        count = []
        output = ""
        for atom in self.atoms:
            if atom.symbol not in types:
                types.append(atom.symbol)
                count.append(1)
            else:
                count[types.index(atom.symbol)] = count[types.index(atom.symbol)] + 1
        if only == 'numbers':
            for item in count:
                output = output + "%i " % item
        elif only == 'letters':
            for item in types:
                output = output + "%s " % item
            output = output + '\n'
        elif only == 'title':
            for item in types:
                output = output + "%s" % item
        else:
            for item in types:
                output = output + "%s %i " % (item, count[types.index(item)])
        return output
    
    def save_as(self, path, file_type='poscar'):
        if file_type == 'poscar':
            outfile = open(path + '/POSCAR', 'w')
            outfile.write(self.atom_counts('title'))
            outfile.write(' - %s\n' % datetime.now())
            outfile.write('%f\n' % self.a0)
            outfile.write(str(self.primitive_cell))
            outfile.write(self.atom_counts('letters'))
            outfile.write(self.atom_counts('numbers'))
            outfile.write("\nDirect\n")
            for atom in self.atoms:
                s = str(atom).split()
                outfile.write("  %s\t%s\t%s\n" % (s[1], s[2], s[3]))
            outfile.close()
        elif file_type == 'xyz':
            pass # Might be added later


    def get_highest_position(self, direction=2): # Return highest value in one direction in direct coordinates
        highest = self.atoms[0].position[direction]
        for atom in self.atoms:
            if atom.position[direction] > highest:
                highest = atom.position[direction]
        return highest

    def get_lowest_position(self, direction=2): # Return lowest value in one direction in direct coordinates
        lowest = self.atoms[0].position[direction]
        for atom in self.atoms:
            if atom.position[direction] < lowest:
                lowest = atom.position[direction]
        return lowest

    def center_positions(self, direction=2): # Doesn't really work...
        diff = 0.5 - (self.get_highest_position(direction) - self.get_lowest_position(direction))/2.
        for atom in self.atoms:
            atom.position[direction] = atom.position[direction] + diff

    def remove_layer(self, highest, direction=2):
        i = 0
        while i < len(self.atoms):
            if round(self.atoms[i].position[direction], 5) == round(highest, 5):
                self.atoms.remove(self.atoms[i])
            else:
                i += 1
        new_highest = self.get_highest_position(direction)
        displacement_factor = 1 - (highest - new_highest)
        for atom in self.atoms:
            atom.position[direction] = atom.position[direction] / displacement_factor
        self.primitive_cell.matrix[direction] = self.primitive_cell.matrix[direction] * displacement_factor

    def change_surface(self, new_direction):
        """Changes the primitive cell and the basis so the new_direction is in the a3-direction
        
        Takes an array as input
        """
        new_a3 = new_direction / self.a0
        print new_a3
        new_direction = self.convert_to_direct(new_a3)
        print new_direction


    def convert_to_direct(self, array):
        return dot(self.primitive_cell.matrix, array)
    
    def convert_to_real(self, array):
        return dot(self.primitive_cell.matrix, array)

def test():
    a0 = 4.2557
    ti = Atom('Ti',array([0.,0.,0.]))
    n = Atom('N',array([0.5,0.5,0.5]))
    primitive_cell = PrimitiveCell(array([0.,0.5,0.5]),array([0.5,0.,0.5]),array([0.5,0.5,0.]))
    super_cell = SuperCell(a0,primitive_cell,[ti,n])
    super_cell.expand_3D((0,0,4))
    print super_cell.primitive_cell
    #super_cell.sort()
    for at in super_cell.atoms: print at
    print "\nHighest: %f\nLowest: %f\n" % (super_cell.get_highest_position(),super_cell.get_lowest_position())
    print "\nAdding vacuum..."
    super_cell.add_vacuum(10)
    print super_cell.primitive_cell
    print (1-super_cell.get_highest_position())*norm(super_cell.primitive_cell.matrix[2])*a0
    for at in super_cell.atoms: print at
    print super_cell.atom_counts('numbers')
    print "\nRemoving layer...\n"
    super_cell.remove_layer(super_cell.get_highest_position())
    print super_cell.primitive_cell
    print (1-super_cell.get_highest_position())*norm(super_cell.primitive_cell.matrix[2])*a0
    for at in super_cell.atoms: print at
    print super_cell.atom_counts('numbers')
    super_cell.center_positions()
    for at in super_cell.atoms: print at
    super_cell.change_surface(array([0 ,0, a0]))
        

if __name__ == '__main__':
    test()