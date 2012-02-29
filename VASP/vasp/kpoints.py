'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''
from linecache import getline
from numpy import array


class Kpoints(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.kpoints = self._extract_kpoints()
        self.mesh_type = self._extract_type()
        self.total_kpoints = (self.kpoints[0] * self.kpoints[1]
                              * self.kpoints[2])

    def __repr__(self):
        # Sets how the Kpoints class object is represented
        return "%ix%ix%i" % (self.kpoints[0], self.kpoints[1], self.kpoints[2])

    def _extract_kpoints(self):
        # Extracts the k-points as an array
        line = getline("%s/KPOINTS" % self.path, 4).split()
        return array([int(line[0]), int(line[1]), int(line[2])])

    def _extract_type(self):
        # Extracts the type of the k-mesh
        return getline("%s/KPOINTS" % self.path, 3).split()[0]
