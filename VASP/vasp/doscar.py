'''
Created on Feb 29, 2012

@author: chtho
'''
from linecache import getline


class Doscar(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.dos = []
        self.fermi_level = 0.
        self._extract_data()

    def _extract_data(self):
        line = getline('%s/DOSCAR' % self.path, 6).split()
        steps = int(line[2])
        self.fermi_level = float(line[3])
        for i in range(7, steps + 7):
            line = getline('%s/DOSCAR' % self.path, i).split()
            self.dos.append((line[0], line[1], line[2]))
