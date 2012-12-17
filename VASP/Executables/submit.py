#!/usr/bin/env python
'''
Created on Apr 17, 2012

@author: chtho
'''
from os import system
from os import getcwd
from os import chdir
from sys import argv
from sys import exit
from socket import getfqdn

from vasp.find import Find

def get_submit_command():
    domain = getfqdn()
    if ".pdc.kth.se" in domain or ".hpc2n.umu.se" in domain:
        return "qsub"
    elif ".nsc.liu.se" in domain or 'neolith' in domain or 'triolith' in domain:
        return "sbatch"
    else:
        return "sbatch"

def main():
    submit_command = get_submit_command()
    resubmit_all = False
    resubmit_none = False
    
    system('clear')
    starting_path = getcwd() 
    if len(argv) != 3:
        print "Error: Specify run file and out put file e.g RUN and OUTCAR\n"
        exit()
    run_file = argv[1]
    out_file = argv[2]
    found_run_files = Find(starting_path, run_file)
    found_out_files = Find(starting_path, out_file)
    
    for path in found_run_files:
        chdir(path)
        if path in found_out_files:
            if resubmit_all or resubmit_none:
                if resubmit_all:
                    print"Submitting file in %s" % path
                    system("%s %s" % (submit_command, run_file))
                else:
                    print "Ignoring file in %s" % path
            else:
                while True:
                    q = raw_input("Resubmit file in %s?\n(y/n or Y/N to apply to all): " % path)
                    if q == 'Y':
                        resubmit_all = True
                        print"Submitting file in %s" % path
                        system("%s %s" % (submit_command, run_file))
                        break
                    elif q == 'y':
                        print"Submitting file in %s" % path
                        system("%s %s" % (submit_command, run_file))
                        break
                    elif q == 'n':
                        break
                    elif q == 'N':
                        resubmit_none = True
                        break
                    else:
                        print "%s is not a valid choice." % q
        else:
            print "Submitting file in %s" % path
            system("%s %s" % (submit_command, run_file))
    
    chdir(starting_path)

if __name__ == '__main__':
    main()
