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

def no_moplecule(file):
    filepath=os.getcwd()+'/'+str(file)+'_O_insert.gro'
    num_lines = sum(1 for line in open(filepath))
    with open(filepath,'r') as f:
        for i,line in enumerate(f):
            if i>1:
                line=line.split()[0]
                line=line.split('D')[0]
                if i==2:
                    a=int(line)
                if i==num_lines-2:
                    b=int(line)
        no_mol=b-a+1
    return no_mol

def top(file, no_mol):
   filepath='./'+str(file)+'.top'
   copyfile('./standard.top', './'+filepath)
   hs = open('./'+filepath,'a')
   txt='DBT'+'   '+str(no_mol)  # need to find way to get extract poroper name
   hs.write(txt)
   hs.close()

file='DBT1'
for i in range(2):
    subprocess.run(['sbatch', './nvt.sh'])  #need nvt.mdp
    time.sleep(5)
    done=check_run_status()
    subprocess.run(['sbatch', './nvt-run.sh'])
    time.sleep(5)
    done=check_run_status()
    time.sleep(10)
    subprocess.run(['sbatch', './insert.sh'])
    time.sleep(10)
    done=check_run_status()
    time.sleep(10)
    no_mol=no_moplecule(file)  ######
    top(file, no_mol)
    time.sleep(5)
    subprocess.run(['sbatch', './em.sh'])  #need min.mdp
    time.sleep(5)
    done=check_run_status()
    subprocess.run(['sbatch', './em-run.sh'])
    time.sleep(5)
    done=check_run_status()
    time.sleep(10)
