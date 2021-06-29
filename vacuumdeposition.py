"""
Created on Wed Jun  9 13:40:27 2021
VACUUM DEPOSITION OF TWO RANDOMLY SELECTED MOLECULES
@author: KL WOON
"""


import subprocess
import time
from shutil import copyfile
import numpy as np
import math
import os
import random as rd
import re
import sys

def check_run_status():
    time.sleep(10)
    read_file=open('./50mCBD-auto.out') # jobname  need to change to auto find
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

def createnewmolecule(molecule):
    copyfile('./go.sh', './insert.sh')
    f1 = open('./insert.sh', 'a+')
    path='./position.dat'
    x=str(rd.uniform(0.0, 8.4)) 
    y=str(rd.uniform(0.0, 8.3))
    with open(path, 'w') as f:
        f.write(x+' '+y+' '+'12.5'+'\n')
    molecule1=str(molecule)+'.gro'
    time.sleep(2)
    moleculebox=str(molecule)+'_box.gro'
    towrite='mpirun -np 2 gmx_mpi insert-molecules -f emptybox.gro -ci '+molecule1+' -ip position.dat -nmol 1 -rot xyz -o '+ moleculebox
    f1.write(towrite)
    f1.close()
    time.sleep(2)


def top(molecule,i):  # this need to rethink
    if i==0:
        copyfile('./complex.top', './complex2.top')
        time.sleep(2)
    f2 = open('./complex2.top', 'a+')
    molecule=str(molecule)
    towrite=molecule+'    '+str(1)+'\n'  #
    f2.write(towrite)
    f2.close()
    time.sleep(2)

def compile():
    copyfile('./go.sh', './compile.sh')
    time.sleep(2)
    f3 = open('./compile.sh', 'a+')
    towrite='mpirun -np 2 gmx_mpi grompp -f nvt.mdp -c tobecopy.gro -r tobecopy.gro -p complex2.top -o nvt.tpr -n index.ndx -maxwarn 3'  #
    f3.write(towrite)
    f3.close()
    time.sleep(2)

def rerun(norerun):
    copyfile('./go.sh', './rerun.sh')
    time.sleep(2)
    f3 = open('./rerun.sh', 'a+')
    if norerun < 3:
        towrite='mpirun -np 2 gmx_mpi grompp -f nvt2.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p complex2.top -o nvt.tpr -n index.ndx -maxwarn 3'  #
    if 6 > norerun >= 3:
        towrite='mpirun -np 2 gmx_mpi grompp -f nvt3.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p complex2.top -o nvt.tpr -n index.ndx -maxwarn 3'  #
    if norerun >= 6:
        towrite='mpirun -np 2 gmx_mpi grompp -f nvt4.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p complex2.top -o nvt.tpr -n index.ndx -maxwarn 3'   #
    f3.write(towrite)
    f3.close()
    fN=open('./N.txt','a')
    fN.write(str(norerun))
    fN.write('\n')
    fN.close()

def create_nvtfile(resid_1, resid_2,norerun):
    if norerun==0:
        copyfile('./nvt-original.mdp', './nvt-write.mdp')  ###
    if norerun!=0 and norerun <3:
        copyfile('./nvt-original2.mdp', './nvt-write.mdp')
    if 6 > norerun >= 3:
        copyfile('./nvt-original3.mdp', './nvt-write.mdp')
    if norerun >= 6:
        copyfile('./nvt-original4.mdp', './nvt-write.mdp')
    with open('./nvt-write.mdp', 'r') as f1:
        lines = f1.readlines()
        if resid_2=='':
            towrite0='tc-grps                 = '+resid_1+'	GRA'+'\n'
            towrite1='tau_t                   = 0.1	0.1'+'\n'
            towrite2='ref_t                   = 300	300'+'\n'
        if resid_2!='':
            towrite0='tc-grps                 = '+resid_1+'_'+resid_2+'	GRA'+'\n'
            towrite1='tau_t                   = 0.1  0.1'+'\n'
            towrite2='ref_t                   = 300  300'+'\n'   
        lines[32]=towrite0
        lines[33]=towrite1
        lines[34]=towrite2
    if norerun==0:
        with open('./nvt.mdp', 'w') as f2:
            f2.writelines(lines[:])   #copy nv
        f2.close()
    if norerun!=0 and norerun <3:
        if resid_2=='':
            towrite0='acc-grps                = '+resid_1+'\n'
            towrite1='accelerate              = 0 0 -0.005'+'\n'
        if resid_2!='':
            towrite0='acc-grps                = '+resid_1+'_'+resid_2+'\n'
            towrite1='accelerate              = 0 0 -0.005'+'\n'
        lines[42]=towrite0
        lines[43]=towrite1
        with open('./nvt2.mdp', 'w') as f3:
            f3.writelines(lines[:])   #copy nv
        f3.close()
    if 6 > norerun >= 3:
        if resid_2=='':
            towrite0='acc-grps                = '+resid_1+'\n'
            towrite1='accelerate              = 0 0 -0.01'+'\n'
        if resid_2!='':
            towrite0='acc-grps                = '+resid_1+'_'+resid_2+'\n'
            towrite1='accelerate              = 0 0 -0.01'+'\n'
        lines[42]=towrite0
        lines[43]=towrite1
        with open('./nvt3.mdp', 'w') as f4:
            f4.writelines(lines[:])   #copy nv
        f4.close()
    if norerun >= 6:
        if resid_2=='':
            towrite0='acc-grps                = '+resid_1+'\n'
            towrite1='accelerate              = 0 0 -0.25'+'\n'
        if resid_2!='':
            towrite0='acc-grps                = '+resid_1+'_'+resid_2+'\n'
            towrite1='accelerate              = 0 0 -0.25'+'\n'
        lines[42]=towrite0
        lines[43]=towrite1
        with open('./nvt4.mdp', 'w') as f5:
            f5.writelines(lines[:])   #copy nv
        f5.close()
    f1.close()

def atomicmass(a):
    if a=='H':
        a=2
    if a=='C':
        a=12.011
    if a=='N':
        a=14.0067
    if a=='O':
        a=15.9994
    if a=='F':
        a=18.998403
    if a=='S':
        a=32.06
    return a*1.661E-27

def finddistance(x1,y1,z1,x2,y2,z2):
    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def sigma(atom,T):
    kb=1.381E-23
    m=atomicmass(atom)
    sig=np.sqrt(kb*T/m)
    return sig*0.001

def togetboxsize(file):    
    with open(file,'r') as f2:
        for line in (f2.readlines()):
            mylastline=line[:-1]
        return mylastline
def findminz(filepath):
    with open(filepath,'r') as f:
        x=[]
        y=[]
        z=[]
        # groatom=[]
        for i,line in enumerate(f):
            if i==1:
                no=int(line)
            if i>1:
                if i<no+2:
                    line=line.split()
                    column1=line[1]
                    atom=column1[0]
                    column2=line[2]
                    column3=line[3]
                    column4=line[4]
                    column5=line[5]
                    z.append(column5)
                    y.append(column4)
                    x.append(column3)
        minz=min(z)
        minz_index=z.index(minz)
        x1=x[minz_index]
        y1=y[minz_index]
        z1=minz
        noatom=int(column2)
        print(x[minz_index], y[minz_index],minz)
    return x1,y1,z1,noatom

def find_translation(i,x1,y1,z1):
    if i==0:
        file='./GRA_sheet_new.gro'
    if i!=0:
        file='./nvt.gro'
    with open(file,'r') as f2:
        x2=[]
        y2=[]
        z2=[]
        groatom2=[]
        d=[]
        for i,line in enumerate(f2):
            if i==1:
                no=int(line)
            if i>1:
                if 10000>=i<no+2:
                    line=line.split()
                    column0=line[0]
                    column1=line[1]
                    column2=line[2]
                    # atom=column1[0]
                    column3=line[3]
                    column4=line[4]
                    column5=line[5]   
                    distance=finddistance(float(x1),float(y1),float(z1),float(column3),float(column4),float(column5))
                    d.append(distance)
                    z2.append(column5)
                    y2.append(column4)
                    x2.append(column3)
                    groatom2.append(column1)
                if 10000<i<no+2:
                    line=line.split()
                    column0=line[0]
                    column1=line[1][-8:-5].strip(' ')
                    column2=line[1][-5:]
                    # atom=column1[0]
                    column3=line[2]
                    column4=line[3]
                    column5=line[4]   
                    distance=finddistance(float(x1),float(y1),float(z1),float(column3),float(column4),float(column5))
                    d.append(distance)
                    z2.append(column5)
                    y2.append(column4)
                    x2.append(column3)
                    groatom2.append(column1)   
        min_d=float(min(d))
        tran_z=min_d-2.00        # z1 needs to fix to be large
        noatom=int(column2)
    return tran_z,noatom,column0  #noatom is how many atoms are there, coumnzero is the last name of the 1st column

                
def createvelocityandfile(filepath,tran_z,noatom,column0,T,molecule):
    molecule=str(molecule)
    ferror.write('This is used to split '+molecule+'\n')
    fN=open('./velocity.gro','w')  # delete previous file
    fN.close()
    with open(filepath,'r') as f:
        z=[]
        x=[]
        y=[]
        z=[]
        vzz=[]
        groatom=[]
        for i,line in enumerate(f):
            if i==1:
                no=int(line)
            if i>1:
                if i<no+2:
                    line=line.split()
                    column1=line[1]
                    atom=column1[0]
                    column2=int(line[2])
                    column3=line[3]
                    column4=line[4]
                    column5=line[5]
                    if column4=='-0.000':  # buggy gromac files generate -0.000
                        column4='0.000'
                    if column3=='-0.000':
                        column3='0.000'
                    z.append(column5)
                    y.append(column4)
                    x.append(column3)
                    groatom.append(column1)
                    new_z=float(column5)-tran_z
                    if float(new_z)>=10.000:
                        column5='  '+str('{0:.3f}'.format(new_z))
                    else:
                        column5='   '+str('{0:.3f}'.format(new_z))
                    vx='{0:.4f}'.format(np.random.normal(0,sigma(atom,T)))
                    vy='{0:.4f}'.format(np.random.normal(0,sigma(atom,T)))
                    vz='{0:.4f}'.format(np.random.normal(-0.05,sigma(atom,T)))
                    vzz.append(float(vz))
                    if float(vx)<0:
                        vx=' '+str(vx)
                    else:
                        vx='  '+str(vx)
                    if float(vy)<0:
                        vy=' '+str(vy)
                    else:
                        vy='  '+str(vy)
                    if float(vz)<0:
                        vz=' '+str(vz)
                    else:
                        vz='  '+str(vz)
                    if column0=='700GRA':
                        mynum=1401
                    if column0!='700GRA':
                        if 'LS12' in column0:          # to split the string, u dont know whether it is LS12 or what
                            mysplit='LS12'  # generalize
                        if 'mCBD' in column0:
                            mysplit='mCBD'
                        mynum=column0.replace(mysplit,'')
                        mynum=int(mynum)+1
                    firstcolumn=str(mynum)+molecule
                    towritefirst=f'{firstcolumn.rjust(9)}'
                    noatoms=str(column2+noatom)
                    if float(column3)<0:
                        column3='  '+str('{0:.3f}'.format(float(column3)))
                    else:
                        column3='   '+str('{0:.3f}'.format(float(column3)))
                    if float(column4)<0:
                        column4='  '+str('{0:.3f}'.format(float(column4)))
                    else:
                        column4='   '+str('{0:.3f}'.format(float(column4)))
                    towritep=column3+column4+column5
                    towrites=vx+vy+vz
                    towritea='   '+f'{column1.rjust(3)}'
                    towritenoa=f'{noatoms.rjust(5)}'
                    with open('./velocity.gro', 'a') as f5:
                        f5.write(towritefirst+towritea+towritenoa+towritep+towrites)
                        f5.write('\n')
    return new_z,np.mean(vzz) 


def cretefinalfile(i,noatom_insert,filepath):
    if i==0:
        file='./GRA_sheet_new.gro'
    if i!=0:
        file='./nvt.gro'
    with open(file, 'r') as f1:
        lines = f1.readlines()
        noofatom=int(lines[1])
        lines[1]=str(noofatom++int(noatom_insert))+'\n'
        currentnoofatom=int(lines[1])
        lines[1]=f'{lines[1].rjust(6)}'
    with open('./tobecopy.gro', 'w') as f2:
        f2.writelines(lines[:-1])
    fin = open('./velocity.gro', 'r')
    data2 = fin.read()
    fout = open('./tobecopy.gro', 'a')
    fout.write(data2)
    mylastline=togetboxsize(filepath)
    fout.write(mylastline)
    time.sleep(5)
    f1.close()
    f2.close()
    fin.close()
    fout.close()
    return currentnoofatom


def readfirstmolecule():   # after the final file is created for top
    with open('./tobecopy.gro', 'r') as f1:
        lines=f1.readlines()
        my701=lines[2802]
        if 'LS12' in my701:
            my701='LS12'
        if 'mCBD' in my701:
            my701='mCBD'
    f1.close()
    return my701
    

def findxyzlastmolecule(filepath,noatom):
    with open(filepath,'r') as f:
        z=[]
        x=[]
        y=[]
        # groatom=[]
        noatom=noatom+1
        for line in (f.readlines() [-noatom:]):
            if len(line)>40:
                line=line.split()
                if len(line)==9:
                    column3=line[3]
                    column4=line[4]
                    column5=line[5]
                    z.append(column5)
                    y.append(column4)
                    x.append(column3)
                if len(line)==8:
                    column3=line[2]
                    column4=line[3]
                    column5=line[4]
                    z.append(column5)
                    y.append(column4)
                    x.append(column3)
    minz=min(z)
    minz_index=z.index(minz)
    x1=x[minz_index]
    y1=y[minz_index]
    z1=minz
    return x1,y1,z1

def finddistance(x1,y1,z1,x2,y2,z2):
    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def hasthemoleculedock(file,x1,y1,z1,noatom):
    with open(file,'r') as f2:
        x2=[]
        y2=[]
        z2=[]
        d=[]
        for i,line in enumerate(f2):
            if i==1:
                no=int(line)
            if i>1:
                if 10000>=i<no+2-noatom:
                    line=line.split()
                    column3=line[3]
                    column4=line[4]
                    column5=line[5]
                    distance=finddistance(float(x1),float(y1),float(z1),float(column3),float(column4),float(column5))
                    d.append(distance)
                    z2.append(column5)
                    y2.append(column4)
                    x2.append(column3)
                if 10000<i<no+2-noatom:
                    line=line.split()
                    column0=line[0]
                    column1=line[1][-8:-5].strip(' ')
                    column2=line[1][-5:]
                    # atom=column1[0]
                    column3=line[2]
                    column4=line[3]
                    column5=line[4]   
                    distance=finddistance(float(x1),float(y1),float(z1),float(column3),float(column4),float(column5))
                    d.append(distance)
                    z2.append(column5)
                    y2.append(column4)
                    x2.append(column3)
        fN=open('./N.txt','a')
        mind=float(min(d))
        fN=open('./N.txt','a')
        fN.write(str(mind))
        fN.write('\n')
        fN.close()
    return mind<0.4

def checkerror(line):
    f10= open('./'+str(line)+'.err','r')
    for i,line in enumerate(f10):
        if 'Fatal error:' in line:
            sys.exit()
    f10.close()


def choicemolecule():
    moleculeList = ['LS12','mCBD']
    molecule=rd.choices(moleculeList, weights=(50, 50))
    molecule=molecule[0]
    if molecule=='LS12':
        mynoatom=54
    if molecule=='mCBD':
        mynoatom=62
    return molecule, mynoatom


def find_top():
    file='./tobecopy.gro'
    with open(file,'r') as f2:
        LS12=0
        mCBD=0
        for i,line in enumerate(f2):
            if i==1:
                no=int(line)
            if i>1:
                if i<no+2:
                    line=line.split()
                    column0=line[0]
                    if 'LS12' in column0:
                        LS12 +=1
                    if 'mCBD' in column0:
                        mCBD +=1
    LS12=int(LS12/54)
    mCBD=int(mCBD/62)
    return LS12,mCBD


def get_job_name(filepath):
    f=open('./'+filepath)
    for i, line in enumerate(f):
        if 'job-name=' in line:
            line2=line.split('=')[1]
    return line2.rstrip()


def append_topology(grofilein,toptoappend,wheretostartfrom):
    f=open('./'+str(grofilein))
    mylist=[]
    for i, line in enumerate(f):
        if i==1:
            no=int(line)
            resrename=''
        if i>1+int(wheretostartfrom):
            if i<no+2:
                line=line.split()
                column0=line[0]
                column0=re.split('(\d+)',column0)
                size=len(column0)
                print(column0[1:2][0])
                resid=''
                for ii in range(2,size):
                    resid =resid+str(column0[ii:ii+1][0])
                mylist=mylist+[(molecule_no,resid)] 
    mylist = list(dict.fromkeys(mylist))
    copyfile('./complex.top', './'+str(toptoappend))
    time.sleep(2)
    f2=open('./'+str(toptoappend),'a')
    resid_2=''
    for i in range(len(mylist)):
        resid_1=str(mylist[0][1])
        which_resid_next=str(mylist[i][1])
        if resid_1 != which_resid_next:
            resid_2 = which_resid_next
        if '.' not in str(mylist[i][1]):
            towrite=str(mylist[i][1])+'   '+'1\n'
            f2.write(towrite)
    f2.close()
    return resid_1,resid_2

def make_python_index(filetobeindex):
    with open('./index.py', 'w') as f:
        f.write('import time'+'\n')
        f.write('import os' +'\n')
        f.write('os.system(\'echo -e \" 3 | 4\\n q\" | gmx_mpi make_ndx -f '+filetobeindex+' -o index.ndx\')'+'\n')
        f.write('time.sleep(5)'+'\n')
        f.write('os.remove(\'#index.ndx.1#\')')
    f.close()


def relaxation(i):
    if i==100:  # for testing  
        a=1
    if i!=100:
        subprocess.run(['sbatch', './compile400K.sh'])
        time.sleep(5)
        job_name=get_job_name('compile400K.sh')
        checkerror(job_name)
        subprocess.run(['sbatch', './run400K.sh'])
        time.sleep(10)
        job_name=get_job_name('run400K.sh')
        checkerror(job_name)
        done=check_run_status()
        subprocess.run(['sbatch', './compilecool.sh'])
        time.sleep(5)
        job_name=get_job_name('compilecool.sh')
        checkerror(job_name)
        subprocess.run(['sbatch', './runcool.sh'])
        time.sleep(10)
        job_name=get_job_name('runcool.sh')
        done=check_run_status()


T=300
new_z=1
myzv=0
goterror=False
fN=open('./N.txt','w')
fN.close()

ferror=open('./error.txt','w') # for testing


while goterror==False:  #
    for i in range(900): 
        if i%100==0 and i!=0:
            relaxation(i)  
        molecule,sizeofmolecule=choicemolecule()
        sizeofmolecule=int(sizeofmolecule)
        filepath='./'+molecule+'_box.gro'
        norerun=0
        while new_z<0.3:
            createnewmolecule(molecule)
            subprocess.run(['sbatch', './insert.sh'])
            done=check_run_status()
            x1,y1,z1,noatom_insert=findminz(filepath)
            tran_z,noatom,column0=find_translation(i,x1,y1,z1)
            while myzv>=0:
                new_z,myzv=createvelocityandfile(filepath,tran_z,noatom,column0,T,molecule)
            myzv=0
            done=check_run_status()
            time.sleep(5)
        createnewmolecule(molecule)
        subprocess.run(['sbatch', './insert.sh'])
        done=check_run_status()
        x1,y1,z1,noatom_insert=findminz(filepath)
        tran_z,noatom,column0=find_translation(i,x1,y1,z1)
        while myzv>=0:
            new_z,myzv=createvelocityandfile(filepath,tran_z,noatom,column0,T,molecule)
        myzv=0
        done=check_run_status()
        time.sleep(5)
        currentnoofatom=cretefinalfile(i,noatom_insert,filepath)
        time.sleep(5)  
        resid_1,resid_2=append_topology('tobecopy.gro','complex2.top',2800)
        create_nvtfile(resid_1,resid_2,norerun)
        time.sleep(5)
        make_python_index('tobecopy.gro') #
        time.sleep(5)  #
        subprocess.run(['sbatch', './index.sh'])   #####
        done=check_run_status()
        compile()
        subprocess.run(['sbatch', './compile.sh'])
        time.sleep(5)
        job_name=get_job_name('compile.sh')
        checkerror(job_name)
        time.sleep(5)
        if i%100!=0:
            subprocess.run(['sbatch', './test.sh'])
            time.sleep(60)
        if i%100==0:
            subprocess.run(['sbatch', './test2.sh'])
            time.sleep(60)
        done=check_run_status()
        job_name=get_job_name('test.sh')
        goterror=checkerror(job_name)
        x1,y1,z1=findxyzlastmolecule('./nvt.gro',sizeofmolecule)  #size of molecule
        time.sleep(5)
        mind=hasthemoleculedock('./nvt.gro',x1,y1,z1,sizeofmolecule)#size of molecule
        while mind==False:
            norerun +=1
            create_nvtfile(resid_1,resid_2,norerun)
            rerun(norerun)
            subprocess.run(['sbatch', './rerun.sh'])
            time.sleep(5)
            job_name=get_job_name('rerun.sh')
            checkerror(job_name)
            subprocess.run(['sbatch', './test.sh'])
            time.sleep(100)
            done=check_run_status()
            job_name=get_job_name('test.sh')
            checkerror(job_name)
            x1,y1,z1=findxyzlastmolecule('./nvt.gro',sizeofmolecule) #size of molecule
            mind=hasthemoleculedock('./nvt.gro',x1,y1,z1,sizeofmolecule) #size of molecule
            if norerun > 12:
                mind=True
       
