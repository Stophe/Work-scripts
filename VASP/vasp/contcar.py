'''
Created on Mar 15, 2012

@author: chtho
'''
from linecache import getline
from numpy import array
from numpy import cross
from numpy.linalg import norm
from sys import exc_info
import numpy as np

from vasp.supercell import SuperCell
from vasp.primitive_cell import PrimitiveCell


class Contcar(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.version = 0
        self.title = ''
        self.selective_dynamics = False
        self.direct_coords = False
        self.counts = []
        self.formula_unit = 0
        self.symbols = []
        self.supercell = SuperCell()
        self.surface_area = 0
        self.coa = 0
        try:
            self._extract_data()
        except:
            print "Error with CONTCAR in: %s" % self.path
            #print exc_info()
            
    def find_adatoms(self):
        # Mark adatoms
        nr_of_adatoms = self._count_adatoms()
        for i in range(1, 1 + nr_of_adatoms):
            self.supercell.atoms[-i].adatom = True
            
    def _count_adatoms(self):
        """
        This function will count atoms as adatoms if there is less atoms on top 
        surface than in the bottom layer.
        
        Accuracy of the rounding is set with decimals variable
        """
        decimals = 5
        
        hp = round(self.supercell.get_highest_position(), decimals)
        atoms_at_hp = 0
        for atom in self.supercell.atoms:
            if round(atom.position[2], decimals) == hp:
                atoms_at_hp += 1
        lp = round(self.supercell.get_lowest_position(), decimals)
        atoms_at_lp = 0
        for atom in self.supercell.atoms:
            if round(atom.position[2], decimals) == lp:
                atoms_at_lp += 1
        if atoms_at_hp < atoms_at_lp:
            return atoms_at_hp
        else:
            return 0

    def _convert_to_direct_coordinates(self):
        print "Running convertion"
        new_sc = SuperCell()
        for atom in self.supercell.atoms:
            new_sc.add(atom.symbol, self.supercell.convert_to_direct(atom.position))
        self.supercell.atoms = new_sc.atoms
        self.direct_coords = True

    def _extract_data(self):
        def _float_list(lst):
            new_lst = []
            for item in lst:
                new_lst.append(float(item))
            return new_lst

        def _int_list(lst):
            new_lst = []
            for item in lst:
                new_lst.append(int(item))
            return new_lst

        if getline("%s/CONTCAR" % self.path, 6).strip().isdigit():
            self.version = 4
            self.counts = _int_list(getline("%s/CONTCAR" % self.path, 6).split())
            self.symbols = ['None'] * len(self.counts)
        else:
            self.version = 5
            self.symbols = getline("%s/CONTCAR" % self.path, 6).split()
            self.counts = _int_list(getline("%s/CONTCAR" % self.path, 7).split())

        maximum = self.counts[0]
        for count in self.counts:
            if count > maximum:
                maximum = count
        self.formula_unit = maximum

        pos_starting_line = 0

        if self.version >= 5:
            if getline("%s/CONTCAR" % self.path, 8)[0] in ['s', 'S']:
                self.selective_dynamics = True
                if  getline("%s/CONTCAR" % self.path, 9)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 10
            else:
                if  getline("%s/CONTCAR" % self.path, 8)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 9
        else:
            if getline("%s/CONTCAR" % self.path, 7)[0] in ['s', 'S']:
                self.selective_dynamics = True
                if  getline("%s/CONTCAR" % self.path, 8)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 9
            else:
                if  getline("%s/CONTCAR" % self.path, 7)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 6

        self.title = getline("%s/CONTCAR" % self.path, 1).rstrip()
        self.supercell.a0 = float(getline("%s/CONTCAR" % self.path, 2).split()[0])
        a1 = _float_list(getline("%s/CONTCAR" % self.path, 3).split())
        a1 = array([a1[0], a1[1], a1[2]])
        a2 = _float_list(getline("%s/CONTCAR" % self.path, 4).split())
        a2 = array([a2[0], a2[1], a2[2]])
        a3 = _float_list(getline("%s/CONTCAR" % self.path, 5).split())
        a3 = array([a3[0], a3[1], a3[2]])
        self.coa = norm(a3)       
        self.supercell.primitive_cell = PrimitiveCell(a1, a2, a3)
        if self.supercell.a0 < 0:
            self.supercell.a0 = (self.supercell.a0/np.linalg.det(self.supercell.primitive_cell.matrix))**(1./3.)
        self.surface_area = self.supercell.a0**2 * norm(cross(a1, a2))
        f = open("%s/CONTCAR" % self.path)
        for i in range(0, len(self.counts)):
            for j in range(pos_starting_line,
                              pos_starting_line + self.counts[i]):
                position = getline("%s/CONTCAR" % self.path, j).split()
                if self.selective_dynamics:
                    relax = position[3:6]
                position = _float_list(position[:3])
                position = array([position[0], position[1], position[2]])
                if self.selective_dynamics:
                    self.supercell.add(self.symbols[i], position,
                                       relaxation=relax)
                else:
                    self.supercell.add(self.symbols[i], position)
            pos_starting_line += self.counts[i]

        f.close()
        if not self.direct_coords:
            self._convert_to_direct_coordinates()
    
    def distance(self, r1, r2):
        delta = np.linalg.norm(self.supercell.convert_to_real(r1 - r2))
        return delta
    
    def _calculate_sqs_repetitions(self, metals, other):
        scx = 0
        scy = 0
        scz = 0
        
        for atom in self.supercell.atoms:
            if (atom.symbol in metals
                  and self.distance(array([0, 0, 0]),
                                  array([atom.position[0], atom.position[1], atom.position[2]])) < 0.5):
                scx += 1
                scy += 1
                scz += 1
            elif (atom.symbol in metals
                  and self.distance(array([0, 0, 0]),
                                  array([atom.position[0], atom.position[1], 0])) < 0.5):
                scz += 1
            elif (atom.symbol in metals
                  and self.distance(array([0, 0, 0]),
                                  array([0, atom.position[1], atom.position[2]])) < 0.5):
                scx += 1
            elif (atom.symbol in metals
                  and self.distance(array([0, 0, 0]),
                                  array([atom.position[0], 0, atom.position[2]])) < 0.5):
                scy += 1

        return (scx, scy, scz)
    
    def calculate_average_u(self, return_all=False):
        metals = ['Al', 'Sc', 'In', 'Y']
        other = ['N']
        sqs_repetitions = self._calculate_sqs_repetitions(metals, other)
        u_list = []
        for atom1 in self.supercell.atoms:
            if atom1.symbol in metals:
                d = 0.
                for atom2 in self.supercell.atoms:
                    if atom2.symbol in other:
                        if (atom2.position[2] > atom1.position[2] 
                            and self.distance(array([atom1.position[0], atom1.position[1], 0]),
                                              array([atom2.position[0], atom2.position[1], 0])) < 0.5):
                            new_d = self.distance(atom1.position, atom2.position) 
                            if d == 0 or new_d < d:
                                d = new_d
                        elif (atom2.position[2] + 1. > atom1.position[2] 
                            and self.distance(array([atom1.position[0], atom1.position[1], 0]),
                                              array([atom2.position[0], atom2.position[1], 0])) < 0.5 ):
                            new_d = self.distance(atom1.position, atom2.position + array([0, 0, 1.]))
                            if d == 0 or new_d < d: 
                                d = new_d
                if d == 0:
                    print "Found no atom to compare with"
                else:
                    u_list.append(d / (self.coa * self.supercell.a0) * sqs_repetitions[2])
        if return_all:
            return u_list
        else:
            return sum(u_list) / len(u_list)

if __name__ == '__main__':
    contcar = Contcar("/Volumes/Macintosh HD 2/git/Work/VASP/Tests/DataExtraction/Ex4")
    print contcar.path
    print contcar.version
    print contcar.title
    print contcar.selective_dynamics
    print contcar.direct_coords
    print contcar.counts
    print contcar.symbols
    print contcar.supercell.primitive_cell
    for atom in contcar.supercell.atoms:
        print atom, atom.relaxation
    contcar2 = Contcar("/Volumes/Macintosh HD 2/git/Work/VASP/Tests/DataExtraction/Ex6")
    print contcar2.symbols
    print contcar2.counts
    for atom in contcar2.supercell.atoms:
        if atom.adatom:
            print atom
