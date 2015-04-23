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
        self.magmom = 0
        self.all_energies = []
        self.iterations = 0
        self._extract_data()

    def _extract_data(self):
        # Extracts the total energy from the last iteration
        f = open("%s/OSZICAR" % (self.path), 'r')
        for line in f:
            if 'E0=' in line:
                self.iterations = int(line.split()[0])  
                self.all_energies.append(float(line.split()[4]))
                if 'mag=' in line:
                    self.magmom = float(line.split()[9])
        f.close()
        if self.all_energies: self.total_energy = self.all_energies[-1]

if __name__ == '__main__':
    path = '/Volumes/Macintosh HD 2/git/Work/VASP/Tests/DataExtraction/Ex6'
    oszicar = Oszicar(path)
    print oszicar.magmom
    print oszicar.all_energies
    print oszicar.total_energy
