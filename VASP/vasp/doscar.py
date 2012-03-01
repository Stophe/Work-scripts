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
        self._extract_data()

    def _extract_data(self):
        steps = int(getline('%s/DOSCAR' % self.path, 6).split()[2])
        for i in range(7, steps):
            line = getline('%s/DOSCAR' % self.path, i).split()
            self.dos.append((line[0], line[1], line[2]))
