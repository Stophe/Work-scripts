'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''
from linecache import getline
from numpy import array
from numpy import cross
from numpy.linalg import norm

from vasp.supercell import SuperCell
from vasp.primitive_cell import PrimitiveCell


class Poscar(object):
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
        self._extract_data()

    def find_adatoms(self):
        # Mark adatoms
        nr_of_adatoms = _count_adatoms()
        for i in range(1, 1 + nr_of_adatoms):
            self.supercell.atoms[-i].adatom = True
    
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
        
        def _count_adatoms():
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
            

        if getline("%s/POSCAR" % self.path, 6).strip().isdigit():
            self.version = 4
            self.counts = _int_list(getline("%s/POSCAR" % self.path, 6).split())
            self.symbols = ['None'] * len(self.counts)
        else:
            self.version = 5
            self.symbols = getline("%s/POSCAR" % self.path, 6).split()
            self.counts = _int_list(getline("%s/POSCAR" % self.path, 7).split())

        maximum = self.counts[0]
        for count in self.counts:
            if count > maximum:
                maximum = count
        self.formula_unit = maximum

        pos_starting_line = 0

        if self.version >= 5:
            if getline("%s/POSCAR" % self.path, 8)[0] in ['s', 'S']:
                self.selective_dynamics = True
                if  getline("%s/POSCAR" % self.path, 9)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 10
            else:
                if  getline("%s/POSCAR" % self.path, 8)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 9
        else:
            if getline("%s/POSCAR" % self.path, 7)[0] in ['s', 'S']:
                self.selective_dynamics = True
                if  getline("%s/POSCAR" % self.path, 8)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 9
            else:
                if  getline("%s/POSCAR" % self.path, 7)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 6

        self.title = getline("%s/POSCAR" % self.path, 1).rstrip()
        self.supercell.a0 = float(getline("%s/POSCAR" % self.path, 2))
        a1 = _float_list(getline("%s/POSCAR" % self.path, 3).split())
        a1 = array([a1[0], a1[1], a1[2]])
        a2 = _float_list(getline("%s/POSCAR" % self.path, 4).split())
        a2 = array([a2[0], a2[1], a2[2]])
        a3 = _float_list(getline("%s/POSCAR" % self.path, 5).split())
        a3 = array([a3[0], a3[1], a3[2]])
        self.surface_area = self.supercell.a0 * 2 * norm(cross(a1, a2))
        self.supercell.primitive_cell = PrimitiveCell(a1, a2, a3)
        f = open("%s/POSCAR" % self.path)
        for i in range(0, len(self.counts)):
            for j in range(pos_starting_line,
                              pos_starting_line + self.counts[i]):
                position = getline("%s/POSCAR" % self.path, j).split()
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

if __name__ == '__main__':
    poscar = Poscar("/Volumes/Macintosh HD 2/git/Work/VASP/Tests/DataExtraction/Ex4")
    print poscar.path
    print poscar.version
    print poscar.title
    print poscar.selective_dynamics
    print poscar.direct_coords
    print poscar.counts
    print poscar.symbols
    print poscar.supercell.primitive_cell
    for atom in poscar.supercell.atoms:
        print atom.adatom
    poscar2 = Poscar("/Volumes/Macintosh HD 2/git/Work/VASP/Tests/DataExtraction/Ex6")
    print poscar2.symbols
    print poscar2.counts
    for atom in poscar2.supercell.atoms:
        if atom.adatom:
            print atom
