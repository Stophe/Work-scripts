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
        self.total_cpu_time = 0
        self.volume = 0
        self._extract_data()

    def _extract_data(self):
        # Extracts the total CPU time in seconds
        f = open("%s/OUTCAR" % (self.path), 'r')
        for line in f:
            if 'volume of cell :' in line:
                self.volume = float(line.split()[4])
            elif 'Total CPU time' in line:
                self.total_cpu_time = line.split()[5]
        f.close()
