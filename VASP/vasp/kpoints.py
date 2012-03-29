'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''
from linecache import getline
from numpy import array


class Kpoints(object):
    '''
    Class for reading and creating KPOINTS files
    '''

    def __init__(self, path, kpoints=(0, 0, 0), mesh_type=''):
        '''
        Constructor
        '''
        self.path = path
        self.kpoints = array(kpoints)
        self.mesh_type = mesh_type
        self.total_kpoints = (self.kpoints[0] * self.kpoints[1]
                              * self.kpoints[2])
        if mesh_type == '':
            self._extract_kpoints()
            self._extract_type()
        else:
            self.create_file

    def __repr__(self):
        # Sets how the Kpoints class object is represented
        return "%ix%ix%i" % tuple(self.kpoints)

    def _extract_kpoints(self):
        # Extracts the k-points as an array
        line = getline("%s/KPOINTS" % self.path, 4).split()
        self.kpoints = array([int(line[0]), int(line[1]), int(line[2])])

    def _extract_type(self):
        # Extracts the type of the k-mesh
        self.mesh_type = getline("%s/KPOINTS" % self.path, 3).split()[0]

    def create_file(self):
        f = open('%s/KPOINTS' % self.path, 'w')
        f.write("%ix%ix%i\n" % tuple(self.kpoints))
        f.write("0\n")
        f.write("%s\n" % self.mesh_type)
        f.write("%i  %i  %i\n" % tuple(self.kpoints))
        f.write("0  0  0")
        f.close()

if __name__ == '__main__':
    path = '/Users/chtho/Desktop'
    kpoints = (1, 1, 1)
    mesh_type = "Monkhorst"
    kps = Kpoints(path, kpoints, mesh_type)
    kps.create_file()
    print kps
