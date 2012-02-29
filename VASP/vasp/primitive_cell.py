'''
Created on Feb 27, 2012

@author: chtho
'''
from numpy import array


class PrimitiveCell(object):
    '''
    classdocs
    '''

    def __init__(self, a1, a2, a3):
        """
        PrimitiveCell is the class for the primitive cell of the structure.
        """
        self.matrix = array([a1, a2, a3])
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3

    def __repr__(self):
        return ("  %f  %f  %f\n  %f  %f  %f\n  %f  %f  %f\n" %
                (self.matrix[0][0], self.matrix[0][1], self.matrix[0][2],
                 self.matrix[1][0], self.matrix[1][1], self.matrix[1][2],
                 self.matrix[2][0], self.matrix[2][1], self.matrix[2][2]))
