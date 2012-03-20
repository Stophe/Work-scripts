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
                position = _float_list(getline("%s/POSCAR" % self.path,
                                               j).split())
                position = array([position[0], position[1], position[2]])
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
        print atom
