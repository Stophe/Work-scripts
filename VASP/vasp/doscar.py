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
        i = 7
        while True:
            line = getline('%s/DOSCAR' % self.path, i).split()
            if len(line) == 3:
                self.dos.append((line[0], line[1], line[2]))
            else:
                break
            i += 1
