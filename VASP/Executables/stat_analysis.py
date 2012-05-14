#!/usr/bin/env python
'''
Created on May 14, 2012

@author: chtho
'''
import pstats


def main():
    f = open('results.txt', 'w')
    s = pstats.Stats('profiledata.txt', stream=f)
    s.sort_stats('cumulative')
    s.print_stats()

if __name__ == '__main__':
    main()