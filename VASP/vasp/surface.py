'''
Created on Feb 27, 2012

@author: Christopher Tholander
'''


class Surface(object):
    '''
    classdocs
    '''

    def __init__(self, supercell):
        '''
        Constructor
        '''
        self.primitive_cell = supercell.primitive_cell
        self.vacuum = 0
        self.atoms = supercell.atoms
