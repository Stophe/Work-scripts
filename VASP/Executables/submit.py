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
from vasp.outcar import Outcar
from vasp.contcar import Contcar

def get_submit_command():
    domain = getfqdn()
    if ".hpc2n.umu.se" in domain:
        return "qsub"
    elif ".nsc.liu.se" in domain or 'neolith' in domain or 'triolith' in domain:
        return "sbatch"
    else:
        return "sbatch"

def main():
    submit_command = get_submit_command()
    resubmit_all = False
    resubmit_none = False
    resubmit_unfinished = False
    
    system('clear')
    starting_path = getcwd() 
    if len(argv) != 3:
        print "Error: Specify run file and program e.g, RUN and vasp\n"
        exit()
    run_file = argv[1]
    if argv[2]:
        program = argv[2]
    else:
        program = "vasp"
    if program == "vasp":
        out_file = "OUTCAR.bz2"
    else:
        print "No outfile specified for that program yet!"
        exit()     
    
    found_run_files = Find(starting_path, [run_file])
    found_out_files = Find(starting_path, [out_file])
    
    for path in found_run_files:
        chdir(path)
        if path in found_out_files:
            if resubmit_all or resubmit_none:
                if resubmit_all:
                    print"Submitting file in %s" % path
                    system("%s %s" % (submit_command, run_file))
                else:
                    print "Ignoring file in %s" % path
            elif resubmit_unfinished:
                if program == "vasp":
                    outcar = Outcar(path)
                    if outcar.total_cpu_time > 0:
                        pass
                    else:
                        print "Updating files in %s" % path
                        system("cp POSCAR old_POSCAR")
                        system("cp CONTCAR old_CONTCAR")
                        if len(Contcar(path).supercell.atoms) > 0:
                            system("cp CONTCAR POSCAR")
                        else:
                            print "Strange CONTCAR in %s" % path
                        system("cp OSZICAR old_OSZICAR")
                        print"Submitting file in %s" % path
                        system("%s %s" % (submit_command, run_file))
                    
            else:
                while True:
                    q = raw_input("Resubmit file in %s?\n(y/n or Y/N to apply to all), RU to resubmit and update unfinished ones: " % path)
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
                    elif q == "RU":
                        resubmit_unfinished = True
                        if program == "vasp":
                            outcar = Outcar(path)
                            if outcar.total_cpu_time > 0:
                                pass
                            else:
                                print "Updating files in %s" % path
                                system("cp POSCAR old_POSCAR")
                                system("cp CONTCAR old_CONTCAR")
                                if len(Contcar(path).supercell.atoms) > 0:
                                    system("cp CONTCAR POSCAR")
                                else:
                                    print "Strange CONTCAR in %s" % path
                                system("cp OSZICAR old_OSZICAR")
                                print"Submitting file in %s" % path
                                system("%s %s" % (submit_command, run_file))
                        break
                    else:
                        print "%s is not a valid choice." % q
        else:
            print "Submitting file in %s" % path
            system("%s %s" % (submit_command, run_file))
    
    chdir(starting_path)

if __name__ == '__main__':
    main()
