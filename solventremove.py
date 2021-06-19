"""
Created -simulating solvent evapuration -spin0coating
@author: KL WOON
"""


import subprocess
import time
from shutil import copyfile
import numpy as np
import math
import os
import random as rd



def check_run_status():
    time.sleep(100)
    read_file=open('./spin-coating.out') # jobname
    for i, line in enumerate(read_file):
        job_id=line.split()[3]
    check_status='squeue -h -j '+ str(job_id)
    process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    while output.__contains__(job_id):
        time.sleep(100)
        process=subprocess.run(check_status, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout 
    return True

def compile(job):
    copyfile('./go.sh', './compile.sh')
    time.sleep(2)
    job=str(job)
    f3 = open('./compile.sh', 'a+')
    if job=='nvt':
        towrite='mpirun -np 2 gmx_mpi grompp -f nvt.mdp -c md.gro -r md.gro -p complex2.top -o nvt.tpr -n index.ndx -maxwarn 3'
    if job=='npt':
        towrite='mpirun -np 2 gmx_mpi grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p complex2.top -o npt.tpr -n index.ndx -maxwarn 3'
    if job=='md':
        towrite='mpirun -np 2 gmx_mpi grompp -f md.mdp -c npt.gro -r npt.gro -t npt.cpt -p complex2.top -o md.tpr -n index.ndx -maxwarn 3'
    f3.write(towrite)
    f3.close()
    time.sleep(5)

def runjob(job,i):
    copyfile('./go.sh', './run.sh')
    time.sleep(2)
    job=str(job)
    f3 = open('./run.sh', 'a+')
    if job=='nvt':
        towrite='mpirun -np 30 gmx_mpi mdrun -v -deffnm nvt'
    if job=='npt':
        towrite='mpirun -np 30 gmx_mpi mdrun -v -deffnm npt'
    if job=='md':
        if i%10==0:
             f3.close()
             copyfile('./go2.sh', './run.sh')
             time.sleep(2)
             f3 = open('./run.sh', 'a+')
        towrite='mpirun -np 30 gmx_mpi mdrun -v -deffnm md'
    f3.write(towrite)
    f3.close()
    time.sleep(2)
    subprocess.run(['sbatch', './run.sh'])


def find_no_solvent_molecule(filepath,solventnoatom):
    file=filepath
    with open(file,'r') as f2:
        OCS=0
        for i,line in enumerate(f2):
            if i==1:
                no=int(line)
            if i>1:
                if i<no+2:
                    line=line.split()
                    column0=line[0]
                    if '9OC5' in column0:
                        OCS +=1
    OCS=int(OCS/solventnoatom)
    return OCS

def create_top(OCS):  # this need to rethink
    copyfile('./complex.top', './complex2.top')  # complex.top must have number of moecules without solvent
    time.sleep(2)
    f2 = open('./complex2.top', 'a+')
    f2.write('9OC5    '+str(OCS))
    f2.close()
    time.sleep(2)

def indexing_solvent(filepath,noatom,residue): # noatom is the bo of atoms of a solvent molecule
    with open(filepath,'r') as f2:
        indexofsolvent=[]
        mysolvent=[]
        residue=str(residue)
        for i,line in enumerate(f2):
            if i==1:
                no=int(line)
            if i>1:
                if 10000<i<no+2:
                    line=line.split()
                    column0=line[0].split(residue)
                    moleculegroup=column0[0]
                    if moleculegroup.isdigit():
                        mysolvent.append(moleculegroup)           
    for i in mysolvent:
        if i not in indexofsolvent:
            indexofsolvent.append(i)
    f2.close()
    return indexofsolvent

def remove_one_solvent(filetoread,filetowrite,solventtoremove, residue,solventnoatom):
    index_toberemoved=str(solventtoremove)+str(residue)
    a_file=open(filetoread,'r')
    lines=a_file.readlines()
    total_atom=int(lines[1])
    lines[1]=str(total_atom-int(solventnoatom))+'\n'
    new_file=open(filetowrite,'w')
    for line in lines:
        if index_toberemoved not in line:
            new_file.write(line)
    a_file.close()
    new_file.close()

def random_remove_one_solvent(filetoread,filetowrite,indexofsolvent,residue,noatom):
    random_solvent=rd.choice(indexofsolvent)
    indexofsolvent.remove(random_solvent)
    remove_one_solvent(filetoread,filetowrite,random_solvent,residue,noatom)
    return indexofsolvent

def remove_solvent(filetoread,filetowrite,indexofsolvent,residue,solventnoatom):
    if len(indexofsolvent)>=100:
        number_toremove=round(0.025*len(indexofsolvent))
    if 10 <= len(indexofsolvent) < 100:
        number_toremove=10
    if len(indexofsolvent)<10:
        number_toremove=len(indexofsolvent)
    for i in range(number_toremove):
        indexofsolvent=random_remove_one_solvent(filetoread,filetowrite,indexofsolvent,residue,solventnoatom)
    return indexofsolvent


solventnoatom=12
residue='9OC5'
filepath='./md.gro'
filetoread=filepath
filetowrite=filepath
indexofsolvent=indexing_solvent(filepath,solventnoatom,residue)

i=0
while len(indexofsolvent)!=0:
    indexofsolvent=remove_solvent(filetoread,filetowrite,indexofsolvent,residue,solventnoatom)
    time.sleep(10)
    OCS=find_no_solvent_molecule(filepath,solventnoatom)
    create_top(OCS)
    subprocess.run(['sbatch', './index.sh'])
    time.sleep(2)
    compile('nvt')
    subprocess.run(['sbatch', './compile.sh'])
    runjob('nvt',i)
    time.sleep(600)
    done=check_run_status()
    compile('npt')
    subprocess.run(['sbatch', './compile.sh'])
    runjob('npt',i)
    time.sleep(600)
    done=check_run_status()
    compile('md')
    subprocess.run(['sbatch', './compile.sh'])
    runjob('md',i)
    time.sleep(600)
    done=check_run_status()
    i=+1







