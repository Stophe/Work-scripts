'''
Created on Mar 28, 2012

@author: chtho
'''
from os import listdir
from os.path import join

class Run(object):
    '''
    Class generating RUN files
    '''

    def __init__(self, path, title='', project=None, walltime=None,
                 nodes=None, vasp_version=None, computer=None, filename_suffix=''):
        '''
        Constructor
        '''
        self.path = path
        self.title = title.replace(' ', '')
        self.project = project
        self.walltime = walltime
        self.nodes = nodes
        self.vasp_version = vasp_version
        self.computer = computer
        self.filename_suffix = filename_suffix
        if nodes == None:
            self._extract_data()

    
    def _extract_data(self):
        dl = listdir(self.path)
        for item in dl:
            if "RUN" in item:
                f_name = item
        f = open(join(self.path, f_name), 'r')
        for line in f:
            if "#PBS -A" in line:
                self.project = line.split()[2]
            elif "#PBS -N" in line:
                self.title = line.split()[2]
            elif "walltime" in line:
                self.walltime = line.split()[2][9:]
            elif "mppwidth" in line:
                self.nodes = int(line.split()[2][9:])
            elif "#SBATCH -J" in line:
                self.title = line.split()[2]
            elif "#SBATCH -N" in line:
                self.nodes = int(line.split()[2])
            elif "#SBATCH -t" in line:
                self.walltime = line.split()[2]
            elif "#SBATCH -U" in line:
                self.project = line.split()[2]
            elif "#SBATCH -A" in line:
                self.project = line[10:]
        f.close()

    def create_file(self):
        if self.computer == 'pdc':
            self._create_PDC_file()
        elif self.computer == 'nsc':
            self._create_NSC_file()
        elif self.computer == 'prace':
            self._create_prace_file()
        elif self.computer == 'hpc2n':
            self._create_HPC2N_file()
        elif self.computer == 'triolith':
            self._create_Triolith_file()
        elif self.computer == 'green':
            self._create_green_file()
        elif self.computer == 'green_risk':
            self._create_green_risk_file()

    def _create_PDC_file(self):
        f = open("%s/RUN%s" % (self.path, self.filename_suffix), 'w')
        f.write("#!/bin/bash\n")
        f.write("#PDC run file\n")
        f.write("#PBS -A %s\n" % self.project)
        f.write("#PBS -N %s\n" % self.title)
        f.write("#PBS -l walltime=%s\n" % self.walltime)
        f.write("#PBS -l mppwidth=%i\n" % self.nodes)
        f.write("#PBS -e error_file.e\n")
        f.write("#PBS -o output_file.o\n")
        f.write('\n' * 2)
        f.write("#Setting correct working directory\n")
        f.write("PERMDIR=$PBS_O_WORKDIR\n")
        f.write("cd ${PERMDIR}\n")
        f.write('\n')
        f.write("#Loading modules\n")
        f.write(". /opt/modules/default/etc/modules.sh\n")
        f.write("module add vasp/%s\n" % self.vasp_version)
        f.write('\n')
        f.write("#Run calculation\n")
        f.write("aprun -n %i /pdc/vol/vasp/%s/vasp > temp.out\n" % (self.nodes,
                                                         self.vasp_version))
        f.close()
        
    def _create_HPC2N_file(self):
        f = open("%s/RUN%s" % (self.path, self.filename_suffix), 'w')
        f.write("#!/bin/bash\n")
        f.write("#PDC run file\n")
        f.write("#PBS -A %s\n" % self.project)
        f.write("#PBS -N %s\n" % self.title)
        f.write("#PBS -l walltime=%s\n" % self.walltime)
        f.write("#PBS -l nodes=%i:ppn=8\n" % self.nodes)
        f.write("#PBS -e error_file.e\n")
        f.write("#PBS -o output_file.o\n")
        f.write('\n' * 2)
        f.write("#Setting correct working directory\n")
        f.write("PERMDIR=$PBS_O_WORKDIR\n")
        f.write("cd ${PERMDIR}\n")
        f.write('\n')
        f.write("#Loading modules\n")
        f.write(". /opt/modules/default/etc/modules.sh\n")
        f.write("module add vasp/%s\n" % self.vasp_version)
        f.write('\n')
        f.write("#Run calculation\n")
        f.write("aprun -n %i /pdc/vol/vasp/%s/vasp > temp.out\n" % (self.nodes,
                                                         self.vasp_version))
        f.close()

    def _create_NSC_file(self):
        f = open("%s/RUN%s" % (self.path, self.filename_suffix), 'w')
        f.write("#!/bin/bash\n")
        f.write("#NSC run file\n")
        f.write("#SBATCH -J %s\n" % self.title)
        f.write("#SBATCH -t %s\n" % self.walltime)
        f.write("#SBATCH -N %i\n" % self.nodes)
        f.write("#SBATCH %s\n" % self.project)
        f.write('\n')
        f.write("#Run calculation\n")
        f.write("mpprun /software/apps/vasp/%s/default/vasp-half" %
                (self.vasp_version))
        
    def _create_green_file(self):
        f = open("%s/RUN%s" % (self.path, self.filename_suffix), 'w')
        f.write("#!/bin/bash\n")
        f.write("#NSC run file\n")
        f.write("#SBATCH -J %s\n" % self.title)
        f.write("#SBATCH -t %s\n" % self.walltime)
        f.write("#SBATCH -N %i\n" % self.nodes)
        f.write("#SBATCH -A %s -p green\n" % self.project)
        f.write('\n')
        f.write("#Run calculation\n")
        f.write("mpprun /software/apps/vasp/%s/default/vasp-half" %
                (self.vasp_version))
        
    def _create_green_risk_file(self):
        f = open("%s/RUN%s" % (self.path, self.filename_suffix), 'w')
        f.write("#!/bin/bash\n")
        f.write("#NSC run file\n")
        f.write("#SBATCH -J %s\n" % self.title)
        f.write("#SBATCH -t %s\n" % self.walltime)
        f.write("#SBATCH -N %i\n" % self.nodes)
        f.write("#SBATCH -A %s -p green_risk\n" % self.project)
        f.write('\n')
        f.write("#Run calculation\n")
        f.write("mpprun /software/apps/vasp/%s/default/vasp-half" %
                (self.vasp_version))
        
    def _create_Triolith_file(self):
        f = open("%s/RUN%s" % (self.path, self.filename_suffix), 'w')
        f.write("#!/bin/bash\n")
        f.write("#Triolith run file\n")
        f.write("#SBATCH -J %s\n" % self.title)
        f.write("#SBATCH -t %s\n" % self.walltime)
        f.write("#SBATCH -N %i\n" % self.nodes)
        f.write("#SBATCH -U %s\n" % self.project)
        f.write('\n')
        f.write("#Run calculation\n")
        f.write("mpprun /software/apps/vasp/%s/build01/vasp-half" %
                (self.vasp_version))
        
    def _create_prace_file(self):
        f = open("%s/RUN%s" % (self.path, self.filename_suffix), 'w')
        f.write("#!/bin/bash\n")
        f.write("#PRACE run file\n")
        f.write("#@ node = %i\n" % self.nodes)
        f.write("#@ tasks_per_node = 32\n")
        f.write("#@ notification = never\n")
        f.write("#@ input = /dev/null\n")
        f.write("#@ output = out.$(jobid)\n")
        f.write("#@ error = error.$(jobid)\n")
        f.write("#@ wall_clock_limit = %s\n" % self.walltime)
        f.write("#@ job_type = parallel\n")
        f.write("#@ network.MPI = sn_all, not_shared, US\n")
        f.write("#@ queue\n")
        f.write('\n')
        f.write("module load vasp/%s\n" % self.vasp_version)
        f.write("DIR=`pwd`\n")
        f.write("cd $DIR\n")
        f.write("vasp\n")
        
        f.close()

if __name__ == '__main__':
    path = '/Users/chtho/Desktop'
    title = 'test'
    project = '-A liu1 -p green'
    walltime = "00:00:00"
    nodes = 1
    vasp_version = "1.1.1"
    Run(path, title, project, walltime, nodes, vasp_version,
        'pdc', '_pdc').create_file()
    Run(path, title, project, walltime, nodes, vasp_version,
        'nsc', '_nsc').create_file()
