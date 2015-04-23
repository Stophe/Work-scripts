'''
Created on Feb 29, 2012

@author: chtho
'''
from linecache import getline
from vasp.outcar import Outcar


class Doscar(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.dos = []
        self.dos_per_atom = []
        self.fermi_level = 0.
        self.bandgap = 0.
        self.max = 0.
        self.min = 0.
        self.steps = 0.
        self.step_size = 0.
        self.tot_nr_of_electrons = 0
        self.tot_nr_of_atoms = 0
        try:
            self._extract_data()
        except:
            print "Error with DOSCAR in: %s\n" % self.path

    def _extract_data(self):

        def _float_list(lst):
            new_list = []
            for item in lst:
                new_list.append(float(item))
            return new_list
        
        self.tot_nr_of_electrons = Outcar(self.path).total_nr_of_electrons

        first = True

        self.tot_nr_of_atoms = int(getline('%s/DOSCAR' % self.path,
                                           1).split()[0])
        line = _float_list(getline('%s/DOSCAR' % self.path, 6).split())
        self.max = line[0]
        self.min = line[1]
        self.steps = int(line[2])
        self.fermi_level = line[3]
        self.step_size = (self.max - self.min) / self.steps
        for i in range(7, self.steps + 7):
            line = getline('%s/DOSCAR' % self.path, i).split()
            line = _float_list(line)
            self.dos.append([line[0], line[1], line[2]])
            if line[2] == float(self.tot_nr_of_electrons):
                if first:
                    first = False
                    lower_bandgap = line[0]
                end_of_bandgap = line[0]
        self.bandgap = end_of_bandgap - lower_bandgap
        self.fermi_level = ((end_of_bandgap - lower_bandgap)
                            / 2. + lower_bandgap)
        last_line = self.steps + 7
        atoms = self.tot_nr_of_atoms
        while atoms:
            temp = []
            tot = 0
            for i in range(last_line + 1, last_line + 1 + self.steps):
                line = getline('%s/DOSCAR' % self.path, i).split()
                line = _float_list(line)
                tot += line[1] + line[2] + line[3]
                temp.append([line[0], line[1], line[2], line[3],
                             line[1] + line[2] + line[3],
                             tot])
            self.dos_per_atom.append(temp)
            last_line += self.steps + 1
            atoms -= 1
