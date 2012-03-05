#!/usr/bin/env python
from os import getcwd, system
from os.path import isdir
import sys
from csv import writer, QUOTE_MINIMAL
from vasp.find import Find
from vasp.outcar import Outcar
from vasp.oszicar import Oszicar
from vasp.poscar import Poscar
from vasp.kpoints import Kpoints
from vasp.incar import Incar
from vasp.doscar import Doscar


def outcar_is_needed():
    """Checks if information from the OUTCAR is needed. Returns True if it is,
    no otherwise.
    """
    possible_settings = ['total_cpu_time', 'volume', 'dos_per_atom']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False


def oszicar_is_needed():
    """Checks if information from the OSZICAR is needed. Returns True if it is,
    no otherwise.
    """
    possible_settings = ['total_energy', 'all_energies']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False


def poscar_is_needed():
    """Checks if information from the POSCAR is needed. Returns True if it is,
    no otherwise.
    """
    possible_settings = ['title', 'formula_unit', 'surface_area',
                         'lattice_constant', 'dos', 'all_energies',
                         'dos_per_atom']
    if len(set(possible_settings).intersection(set(sys.argv))) > 0:
        return True
    else:
        return False


def kpoints_is_needed():
    """Checks if information from the KPOINTS is needed. Returns True if it is,
    no otherwise.
    """
    possible_settings = ['kpoints', 'kpoint_type', 'total_kpoints']
    if set(possible_settings).intersection(set(sys.argv)):
        return True
    else:
        return False


def incar_is_needed():
    """Checks if information from the INCAR is needed. Returns true if it is,
    no otherwise.
    """
    possible_settings = ['encut']
    if set(possible_settings).intersection(set(sys.argv)):
        return True
    else:
        return False


def doscar_is_needed():
    """Checks if information from the INCAR is needed. Returns true if it is,
    no otherwise.
    """
    possible_settings = ['dos', 'dos_per_atom']
    if set(possible_settings).intersection(set(sys.argv)):
        return True
    else:
        return False


def main():
    """
    The main function. Extracts the data specified in the input arguments.

    If no argument is given the default is to get all data.
    If a path is given, that will be used as the current directory.
    """
    current_path = getcwd()
    if len(sys.argv) == 1:
        sys.argv = sys.argv + ['kpoints', 'kpoint_type', 'total_kpoints',
                               'title', 'formula_unit',
                               'total_energy', 'all_energies',
                               'total_cpu_time', 'encut', 'surface_area',
                               'print', 'dos']
    elif isdir(sys.argv[1]):
        current_path = sys.argv[1]
    rf = open('%s/results.csv' % current_path, 'wb')
    result_csv_file = writer(rf, delimiter=',', quotechar='|',
                             quoting=QUOTE_MINIMAL)

    find = Find(current_path, 'OUTCAR')
    for path in find.paths:
        if outcar_is_needed(): outcar = Outcar(path)
        if oszicar_is_needed(): oszicar = Oszicar(path)
        if poscar_is_needed(): poscar = Poscar(path)
        if kpoints_is_needed(): kpoints = Kpoints(path)
        if incar_is_needed(): incar = Incar(path)
        if doscar_is_needed(): doscar = Doscar(path)
        results = []
        
        for argument in sys.argv:
            if argument == 'title':
                results.append(poscar.title)
            elif argument == 'lattice_constant':
                results.append(poscar.a0)
            elif argument == 'surface_area':
                results.append(poscar.surface_area)
            elif argument == 'formula_unit':
                results.append(poscar.formula_unit)
            elif argument == 'total_energy':
                results.append(oszicar.total_energy)
            elif argument == 'all_energies':
                f = open('%s/all_energies.csv' % current_path, 'wb')
                energy_csv_file = writer(f, delimiter=',', quotechar='|',
                                 quoting=QUOTE_MINIMAL)
                energy_csv_file.writerow([poscar.title] + oszicar.all_energies)
                f.close()
            elif argument == 'total_cpu_time':
                results.append(outcar.total_cpu_time)
            elif argument == 'volume':
                results.append(outcar.volume)
            elif argument == 'kpoints':
                results.append(kpoints)
            elif argument == 'total_kpoints':
                results.append(kpoints.total_kpoints)
            elif argument == 'kpoint_type':
                results.append(kpoints.mesh_type)
            elif argument == 'encut':
                results.append(incar.encut)
            elif argument == 'dos':
                f = open('%s/dos.csv' % current_path, 'w')
                f.write("%f\n" % doscar.fermi_level)
                for line in doscar.dos:
                    f.write("%s,%s,%s\n" % (line[0], line[1], line[2]))
                f.close()
            elif argument == 'dos_per_atom':
                i = 0
                line = 0
                for count in poscar.counts:
                    int_dos = [[0] * 3] * doscar.steps
                    f = open('%s/dos%s.csv' % (current_path, outcar.atom_symbols[i]), 'w')
                    dos_csv_file = writer(f, delimiter=',', quotechar='|',
                                 quoting=QUOTE_MINIMAL)
                    f.write("%s %i\n" % (outcar.atom_symbols[i], count))
                    for atom in range(0, count):
                        for energy in range(0, len(doscar.dos_per_atom[line + atom])):
                            int_dos[energy] = [doscar.dos_per_atom[line + atom][energy][0],
                                               int_dos[energy][1] + doscar.dos_per_atom[line + atom][energy][4],
                                               int_dos[energy][2] + doscar.dos_per_atom[line + atom][energy][5]]
                    for row in int_dos:
                        dos_csv_file.writerow(row)
                    f.close()
                    line += count - 1
                    i += 1  # Choose correct symbol

        result_csv_file.writerow(results)
    rf.close()

    
    if 'print' in sys.argv: 
        system('/bin/cat "%s/results.csv"' % current_path)

if __name__ == '__main__':
    main()
