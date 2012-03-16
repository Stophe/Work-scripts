'''
Created on Mar 15, 2012

@author: chtho
'''
from linecache import getline
from numpy import array

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
        self.symbols = []
        self.supercell = SuperCell()
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

        if getline("%s/CONTCAR" % self.path, 6).strip().isdigit():
            self.version = 4
            self.counts = _int_list(getline("%s/CONTCAR" % self.path, 6).split())
            self.symbols = ['None'] * len(self.counts)
        else:
            self.version = 5
            self.symbols = getline("%s/CONTCAR" % self.path, 6).split()
            self.counts = _int_list(getline("%s/CONTCAR" % self.path, 7).split())

        pos_starting_line = 0

        if self.version >= 5:
            if getline("%s/CONTCAR" % self.path, 8)[0] in ['s', 'S']:
                self.selective_dynamics = True
                if  getline("%s/CONTCAR" % self.path, 9)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 10
        else:
            if getline("%s/CONTCAR" % self.path, 7)[0] in ['s', 'S']:
                self.selective_dynamics = True
                if  getline("%s/CONTCAR" % self.path, 8)[0] in ['D', 'd']:
                    self.direct_coords = True
                pos_starting_line = 9

        self.title = getline("%s/CONTCAR" % self.path, 1).rstrip()
        self.supercell.a0 = float(getline("%s/CONTCAR" % self.path, 2))
        a1 = _float_list(getline("%s/CONTCAR" % self.path, 3).split())
        a1 = array([a1[0], a1[1], a1[2]])
        a2 = _float_list(getline("%s/CONTCAR" % self.path, 4).split())
        a2 = array([a2[0], a2[1], a2[2]])
        a3 = _float_list(getline("%s/CONTCAR" % self.path, 5).split())
        a3 = array([a3[0], a3[1], a3[2]])
        self.supercell.primitive_cell = PrimitiveCell(a1, a2, a3)
        f = open("%s/CONTCAR" % self.path)
        for i in range(0, len(self.counts)):
            for j in range(pos_starting_line,
                              pos_starting_line + self.counts[i]):
                position = _float_list(getline("%s/CONTCAR" % self.path,
                                               j).split())
                position = array([position[0], position[1], position[2]])
                self.supercell.add(self.symbols[i], position)
            pos_starting_line += self.counts[i]

        f.close()

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
        print atom

