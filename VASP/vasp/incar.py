'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''


class Incar(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.encut = 0
        self.extract_data()

    def extract_data(self):
        f = open("%s/INCAR" % self.path, 'r')
        for line in f:
            if 'ENCUT' in line and '#ENCUT' not in line:
                self.encut = line.split('=')[1][:-1]
