'''
Created on Feb 27, 2012

@author: chtho
'''
from numpy import array
from numpy import asmatrix


class PrimitiveCell(object):
    '''
    classdocs
    '''

    def __init__(self, a1, a2, a3):
        """
        PrimitiveCell is the class for the primitive cell of the structure.
        """
        self.matrix = asmatrix(array([a1, a2, a3]))
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3

    def __repr__(self):
        return ' ' + str(self.matrix).replace('[', '').replace(']',  '') + '\n'


if __name__ == '__main__':
    pc = PrimitiveCell(array([1, 0, 0]), array([0, 1, 0]), array([0, 0, 1]))
    print pc
