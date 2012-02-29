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

    def __repr__(self):
        return "%s  %f  %f  %f" % (self.symbol, self.position[0],
                                   self.position[1], self.position[2])
