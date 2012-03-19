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

    def __init__(self, a1=array([0, 0, 0]), a2=array([0, 0, 0]),
                 a3=array([0, 0, 0])):
        """
        PrimitiveCell is the class for the primitive cell of the structure.
        """
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.matrix = asmatrix(array([self.a1, self.a2, self.a3]))

    def __repr__(self):
        l1 = "  %3.9f  %3.9f  %3.9f\n" %\
                (self.matrix[0, 0], self.matrix[0, 1], self.matrix[0, 2])
        l2 = "  %3.9f  %3.9f  %3.9f\n" %\
                (self.matrix[1, 0], self.matrix[1, 1], self.matrix[1, 2])
        l3 = "  %3.9f  %3.9f  %3.9f\n" %\
                (self.matrix[2, 0], self.matrix[2, 1], self.matrix[2, 2])
        return l1 + l2 + l3

    def __str__(self):
        l1 = "  %3.9f  %3.9f  %3.9f\n" %\
                (self.matrix[0, 0], self.matrix[0, 1], self.matrix[0, 2])
        l2 = "  %3.9f  %3.9f  %3.9f\n" %\
                (self.matrix[1, 0], self.matrix[1, 1], self.matrix[1, 2])
        l3 = "  %3.9f  %3.9f  %3.9f\n" %\
                (self.matrix[2, 0], self.matrix[2, 1], self.matrix[2, 2])
        return l1 + l2 + l3

    def update_matrix(self):
        self.matrix = asmatrix(array([self.a1, self.a2, self.a3]))


if __name__ == '__main__':
    pc = PrimitiveCell(array([1.00000, 0, 0]), array([0, 1, 0]), array([0, 0, 1]))
    print pc
