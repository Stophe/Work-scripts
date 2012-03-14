'''
Created on Feb 27, 2012

@author: chtho
'''
from numpy import array


class Atom(object):
    '''
    classdocs
    '''

    def __init__(self, symbol, array=array([0., 0., 0.])):
        """
        Atom initiates with an atomic symbol and position array given in
        direct coordinates.
        """
        if len(symbol) < 2:
            self.symbol = symbol + " "
        elif len(symbol) > 2:
                self.symbol = symbol[0:1]
        else:
            self.symbol = symbol
        self.position = array
        self.relaxation = ['T', 'T', 'T']

    def __repr__(self):
        return "%s  %.9f  %.9f  %.9f" % (self.symbol, self.position[0],
                                         self.position[1], self.position[2])

    def __str__(self):
        return "  %.9f  %.9f  %.9f" % (self.position[0],
                                         self.position[1], self.position[2])

    def str_with_relaxation(self):
        return "  %.9f  %.9f  %.9f  %s  %s  %s" %\
            (self.position[0], self.position[1], self.position[2],
             self.relaxation[0], self.relaxation[1], self.relaxation[2])

if __name__ == '__main__':
    atom = Atom('Ti', array([1, 1, 1]))
    print atom
    print atom.str_with_relaxation()
