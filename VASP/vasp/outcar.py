'''
Created on Feb 27, 2012

@author: chtho
'''

class Outcar(object):
    '''
    Class for extracting data from OUTCAR files
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.nodes = 0
        self.atom_symbols = []
        self.total_nr_of_ions = 0
        self.total_nr_of_electrons = 0
        self.total_cpu_time = 0
        self.volume = 0
        self.encut = 0
        self.kpoints = (0, 0, 0)
        self.nkpts = 0
        self._extract_data()
        self.total_kpoints = sum(self.kpoints)

    def _extract_data(self):
        # Extracts the data from the OUTCAR file
        f = open("%s/OUTCAR" % (self.path), 'r')
        for line in f:
            if 'running on' in line and 'image' not in line:
                self.nodes = int(float(line.split()[2]))
            elif 'VRHFIN' in line:
                line = line.split()[1]
                self.atom_symbols.append(line[1:-1])
            elif 'NIONS' in line:
                line = line.split()
                self.total_nr_of_ions = int(float(line[11]))
            elif 'NELECT' in line:
                self.total_nr_of_electrons = int(float(line.split()[2]))
            elif 'ENCUT' in line:
                self.encut = line.split()[2]
            elif 'KPOINTS' in line:
                ln = line.split()[1].replace('x', ' ').split()
                self.kpoints = (int(ln[0]), int(ln[1]), int(ln[2]))
            elif 'NKPTS' in line:
                self.nkpts = int(line.split()[3])

        try:
            f.seek(-10000, 2)
        except:
            print self.path

        for line in f:
            if 'volume of cell :' in line:
                self.volume = float(line.split()[4])
            elif 'Total CPU time' in line:
                self.total_cpu_time = line.split()[5]
        f.close()
