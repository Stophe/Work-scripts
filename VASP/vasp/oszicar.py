'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''


class Oszicar(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.total_energy = 0
        self.all_energies = []
        self._extract_data()

    def _extract_data(self):
        # Extracts the total energy from the last iteration
        f = open("%s/OSZICAR" % (self.path), 'r')
        for line in f:
            if 'E0=' in line:
                self.all_energies.append(float(line.split()[4]))
        f.close()
        if self.all_energies: self.total_energy = self.all_energies[-1]
