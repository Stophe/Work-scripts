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
    possible_settings = ['dos', 'dos_per_atom', 'bandgap']
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
        col_titles = []
        
        for argument in sys.argv:
            if argument == 'title':
                col_titles.append('Title')
                results.append(poscar.title)
            elif argument == 'lattice_constant':
                col_titles.append('a0 [Ang]')
                results.append(poscar.a0)
            elif argument == 'surface_area':
                col_titles.append('Surface Area [Ang^2]')
                results.append(poscar.surface_area)
            elif argument == 'formula_unit':
                col_titles.append('Formula unit')
                results.append(poscar.formula_unit)
            elif argument == 'total_energy':
                col_titles.append('Total Energy [eV]')
                results.append(oszicar.total_energy)
            elif argument == 'all_energies':
                f = open('%s/all_energies.csv' % current_path, 'wb')
                energy_csv_file = writer(f, delimiter=',', quotechar='|',
                                 quoting=QUOTE_MINIMAL)
                energy_csv_file.writerow([poscar.title] + oszicar.all_energies)
                f.close()
            elif argument == 'total_cpu_time':
                col_titles.append('Total CPU time')
                results.append(outcar.total_cpu_time)
            elif argument == 'volume':
                col_titles.append('Volume [Ang^3]')
                results.append(outcar.volume)
            elif argument == 'kpoints':
                col_titles.append('K-points')
                results.append(kpoints)
            elif argument == 'total_kpoints':
                col_titles.append('Total K-points')
                results.append(kpoints.total_kpoints)
            elif argument == 'kpoint_type':
                col_titles.append('K-mesh type')
                results.append(kpoints.mesh_type)
            elif argument == 'encut':
                col_titles.append('ENCUT')
                results.append(incar.encut)
            elif argument == 'bandgap':
                col_titles.append('Bandgap [eV]')
                results.append(doscar.bandgap)
            elif argument == 'dos':
                f = open('%s/dos.csv' % current_path, 'w')
                f.write("Fermi level,Bandgap\n")
                f.write("%f,%f\n" % (doscar.fermi_level, doscar.bandgap))
                f.write("Energy,DOS,Integrated DOS\n")
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
                    dos_csv_file.writerow(['Symbol', 'Count'])
                    dos_csv_file.writerow([outcar.atom_symbols[i], count])
                    for atom in range(line, line + count):
                        for energy in range(0, doscar.steps):
                            int_dos[energy] = [doscar.dos_per_atom[atom][energy][0],
                                               int_dos[energy][1] + doscar.dos_per_atom[atom][energy][4],
                                               int_dos[energy][2] + doscar.dos_per_atom[atom][energy][5]]
                    dos_csv_file.writerow(['Energy', 'DOS', 'Integrated DOS'])
                    for row in int_dos:
                        dos_csv_file.writerow(row)
                    f.close()
                    line += count
                    i += 1  # Choose correct symbol

        result_csv_file.writerow(col_titles)
        result_csv_file.writerow(results)
    rf.close()

    
    if 'print' in sys.argv: 
        system('/bin/cat "%s/results.csv"' % current_path)

if __name__ == '__main__':
    main()
