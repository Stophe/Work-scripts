#!/usr/bin/env python
'''
Created on Apr 2, 2012

@author: chtho
'''
from os import system
from sys import argv
from socket import getfqdn


if __name__ == '__main__':
    domain = getfqdn()
    if len(argv) < 4:
        if ".pdc.kth.se" in domain:
            for i in range(int(argv[1]), int(argv[2]) + 1):
                system("qdel %s.basslet.pdc.kth.se" % i)
        elif ".nsc.liu.se" in domain:
            for i in range(int(argv[1]), int(argv[2]) + 1):
                system("scancel %i" % i)
    else:
        print "Give start and stop value as arguments!\n"