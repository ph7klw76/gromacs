#convert convertxyztopdb.py using  python and check mistakes
#update itps with name 3letter and charge
#update standard.top
import subprocess
import time
from shutil import copyfile
import numpy as np
import math
import os

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

def no_moplecule(file,residue):
    filepath=os.getcwd()+'/'+str(file)+'.gro'
    a_file=open(filepath, 'r')
    lines=a_file.readlines()
    third=int(lines[2].split(residue)[0])
    last_lines=lines[-2:-1]
    last_lines=int(last_lines[0].split(residue)[0])+1-third   #need to change if it starts with zero, u need to add, sometimes it is zero need program to ensure that
    return last_lines

def top(file, no_mol,res):
   filepath='./'+str(file)+'.top'
   copyfile('./standard.top', './'+filepath)
   hs = open('./'+filepath,'a')
   txt=res+'   '+str(no_mol)  # need to find way to get extract poroper name
   hs.write(txt)
   hs.close()

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

a_file=open('./CN1.pdb', 'r')
lines=a_file.readlines()
residue=lines[4].split()[3]
compilee('gmx_mpi editconf -f '+residue+'.pdb -o CN1.gro','convert.sh')
compilee('mpirun gmx_mpi editconf -f '+residue+'.gro -o '+residue+'-O.gro -box 10 10 10 -center 5 5 5','box.sh')
compilee('gmx_mpi insert-molecules -f '+residue+'-O.gro -ci '+residue+'.gro -nmol 10000 -rot xyz -o '+residue+'-b.gro','insert-start.sh')

file=residue+'-b'  # residue must be only 3 letter
for i in range(10):
    no_mol=no_moplecule(file,residue)  ######
    top(file, no_mol,residue)
    time.sleep(5)
    compilee('gmx_mpi grompp -f minim.mdp -c '+residue+'-b.gro -r '+residue+'-b.gro -p '+residue+'-b.top -o em.tpr -maxwarn 4','em.sh')
    run('mpirun -np 32 gmx_mpi mdrun -v -deffnm em','em-run.sh')  #might want to know no processor
    compilee('gmx_mpi grompp -f nvt.mdp -c em.gro -r em.gro -p '+residue+'-b.top -o nvt.tpr -maxwarn 3','nvt.sh')
    run('mpirun -np 32 gmx_mpi mdrun -v -deffnm nvt','nvt-run.sh') 
    compilee('gmx_mpi insert-molecules -f nvt.gro -ci '+residue+'.gro -nmol 50000 -rot xyz -o '+residue+'-b.gro','insert.sh')
    m=howmanyadded()
    if m<3:
        exit()
