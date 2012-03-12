'''
Created on Feb 27, 2012

@author: chtho
'''


class Outcar(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.tot_nr_of_electrons = 0
        self.total_cpu_time = 0
        self.volume = 0
        self.atom_symbols = []
        self._extract_data()

    def _extract_data(self):
        # Extracts the total CPU time in seconds
        f = open("%s/OUTCAR" % (self.path), 'r')
        for line in f:
            if 'VRHFIN' in line:
                line = line.split()[1]
                self.atom_symbols.append(line[1:-1])
            elif 'NELECT' in line:
                self.tot_nr_of_electrons = int(float(line.split()[2]))
            elif 'volume of cell :' in line:
                self.volume = float(line.split()[4])
            elif 'Total CPU time' in line:
                self.total_cpu_time = line.split()[5]
        f.close()
