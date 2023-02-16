#convert xyz to pdb using  python and check mistakes
#update tips with name 3letter and charge
#update standard.top
# need to change no_moplecule(file)
import subprocess
import time
from shutil import copyfile
import numpy as np
import math
import os
import io
import sys

def check_run_status():
    time.sleep(10)
    read_file=open('./automation.out') # jobname
    for i, line in enumerate(read_file):
        job_id=line.split()[3]
    check_status='squeue -h -j '+ str(job_id)
    process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    while output.__contains__(job_id):
        time.sleep(10)
        process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout 
    return True

def no_moplecule(file,res):
    filepath=os.getcwd()+'/'+str(file)+'.gro'
    a_file=open(filepath, 'r')
    lines=a_file.readlines()
    first=lines[78111].split()[0].split(res)[0]    ###############change
    last=lines[-2:-1][0].split()[0].split(res)[0]
    number=int(last)-int(first)+1    
    return number

def top(file, no_mol,res):
   filepath='./'+str(file)+'.top'
   copyfile('./standard.top', './'+filepath)
   hs = open('./'+filepath,'a')
   txt=res+'   '+str(no_mol)  # need to find way to get extract poroper name
   hs.write(txt)
   hs.close()


def make_sh_file1(code):
    sh= open('./compile.sh','w')
    sh.write('module load gromacs/gromacs-2021.2'+'\n')
    sh.write(code)
    sh.close()
    filename = './gromacs.err'
    with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
        process = subprocess.Popen('source compile.sh'+'; env -0',shell=True, executable='/bin/bash',stdout=writer)
        while process.poll() is None:
            sys.stdout.write(str(reader.read()))
            time.sleep(5)
        # Read the remaining
        sys.stdout.write(str(reader.read()))

def make_sh_file(code):
    sh= open('./compile.sh','w')
    sh.write('module load gromacs/gromacs-2021.2'+'\n')
    sh.write(code)
    sh.close()
    filename = './gromacs.err'
    output = subprocess.check_output('source compile.sh'+'; env -0',shell=True, executable='/bin/bash')

def compilee(txt,job):  #must be string job with extension
   copyfile('./compile.sh', './'+job)
   hs = open('./'+job,'a')
   hs.write(txt)
   hs.close()
   subprocess.run(['sbatch', './'+job])
   time.sleep(5)
   done=check_run_status()
   hs = open('./gromacs.err','r')
   for i, line in enumerate(hs):
       if line=='Fatal error:':
           raise SystemExit

def run(txt,job):  #must be string job with extension
   copyfile('./run.sh', './'+job)
   hs = open('./'+job,'a')
   hs.write(txt)
   hs.close()
   subprocess.run(['sbatch', './'+job])
   time.sleep(10)
   done=check_run_status()
   hs = open('./gromacs.err','r')
   for i, line in enumerate(hs):
       if line=='Fatal error:':
           raise SystemExit
       if line=='Error in user input:':
           raise SystemExit

def howmanyadded():
    hs = open('./gromacs.err','r')
    for i, line in enumerate(hs):
        if 'Added' in line:
            addedm=int(line.split()[1])
    return addedm


file='DEPEPO-box' # residue must be only 3 letter
residue='J8JX'
for i in range(20):
    no_mol=no_moplecule(file,residue)  ######
    top(file, no_mol,residue)
    time.sleep(5)
    make_sh_file('gmx_mpi grompp -f minim.mdp -c '+file+'.gro -r '+file+'.gro -p '+file+'.top -o em.tpr -maxwarn 4')
    time.sleep(5)
    make_sh_file('mpirun gmx_mpi mdrun -v -deffnm em -ntomp 1')
    time.sleep(5)
    make_sh_file('gmx_mpi grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr -maxwarn 3')
    time.sleep(5)
    make_sh_file('mpirun gmx_mpi mdrun -v -deffnm nvt -ntomp 1')
    time.sleep(5)
    make_sh_file('gmx_mpi insert-molecules -f nvt.gro -ci '+residue+'.gro -nmol 50000 -rot xyz -o '+file+'.gro')
    time.sleep(5)
#    compilee('gmx_mpi grompp -f nvt.mdp -c em.gro -r em.gro -p '+residue+'-b.top -o nvt.tpr -maxwarn 3','nvt.sh')
#    run('mpirun -np 32 gmx_mpi mdrun -v -deffnm nvt','nvt-run.sh') 
#    compilee('gmx_mpi grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p CN2-b.top -o npt.tpr -maxwarn 3','npt.sh')
#    run('mpirun -np 32 gmx_mpi mdrun -v -deffnm npt','npt-run.sh') 
#    compilee('gmx_mpi insert-molecules -f nvt.gro -ci '+residue+'.gro -nmol 50000 -rot xyz -o '+residue+'-b.gro','insert.sh')
#    m=howmanyadded()
#    if m<2:
#        exit()
