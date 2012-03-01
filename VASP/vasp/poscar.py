'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''
from linecache import getline
from linecache import clearcache
from numpy import array
from numpy import cross
from numpy.linalg import norm


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
        self.title = ""
        self.formula_unit = 0
        self.a0 = 0
        self.a1 = array([0, 0, 0])
        self.a2 = array([0, 0, 0])
        self.a3 = array([0, 0, 0])
        self.surface_area = 0
        self._extract_data()

    def _extract_data(self):
        line = getline("%s/POSCAR" % (self.path), 8).split()[0]
        if line[0] in ['K', 'k', 'C', 'c', 'D', 'd']:
            self.version = 5
        else:
            self.version = 4

        # Extracts the title line of the POSCAR
        self.title = getline("%s/POSCAR" % (self.path), 1)[:-1]

        # Extracts the lattice constant
        self.a0 = float(getline("%s/POSCAR" % (self.path), 2).split()[0])

        # Extracts the unitcell vectors as arrays
        split_line = getline("%s/POSCAR" % (self.path), 3).split()
        self.a1 = array([float(split_line[0]), float(split_line[1]),
                         float(split_line[2])])
        split_line = getline("%s/POSCAR" % (self.path), 4).split()
        self.a2 = array([float(split_line[0]), float(split_line[1]),
                         float(split_line[2])])
        split_line = getline("%s/POSCAR" % (self.path), 5).split()
        self.a3 = array([float(split_line[0]), float(split_line[1]),
                         float(split_line[2])])

        # Calculates the surface area. Assuming the surface is in the
        # a3 direction
        self.surface_area = self.a0 * 2 * norm(cross(self.a1, self.a2))

        # Extracts the formula unit from the POSCAR
        # (by getting the most occurring atom type)
        if self.version == 5:
            counts = getline("%s/POSCAR" % (self.path), 7).split()
        else:
            counts = getline("%s/POSCAR" % (self.path), 6).split()
        maximum = counts[0]
        for count in counts:
            if count > maximum: maximum = count
        self.formula_unit = maximum
            
        
        clearcache()    