#!/usr/bin/env python
'''
Created on Apr 2, 2012

@author: chtho
'''
from os import system
from sys import argv


if __name__ == '__main__':
    if len(argv) < 4:
        for i in range(int(argv[1]), int(argv[2]) + 1):
            system("qdel %s.basslet.pdc.kth.se" % i)
    else:
        print "Give start and stop value as arguments!\n"