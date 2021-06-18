import subprocess
import time
from shutil import copyfile
import numpy as np
import math
import os
import random as rd



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

def createnewmolecule():
    copyfile('./go.sh', './insert.sh')
    f1 = open('./insert.sh', 'a+')
    path='./position.dat'
    x=str(rd.uniform(0.0, 8.4)) 
    y=str(rd.uniform(0.0, 8.3))
    with open(path, 'w') as f:
        f.write(x+' '+y+' '+'17.0'+'\n')
    time.sleep(2)
    towrite='mpirun -np 2 gmx_mpi insert-molecules -f emptybox.gro -ci LS12.gro -ip position.dat -nmol 1 -rot xyz -o LS12_box.gro'
    f1.write(towrite)
    f1.close()
    time.sleep(2)

def top(n):
    copyfile('./complex.top', './complex2.top')
    time.sleep(2)
    f2 = open('./complex2.top', 'a+')
    n=(n-2800)/54
    n=int(n)
    towrite='LS12	'+str(n)  #
    f2.write(towrite)
    f2.close()
    time.sleep(2)

def compile():
    copyfile('./go.sh', './compile.sh')
    time.sleep(2)
    f3 = open('./compile.sh', 'a+')
    towrite='mpirun -np 2 gmx_mpi grompp -f nvt.mdp -c tobecopy.gro -r tobecopy.gro -p complex2.top -o nvt.tpr -maxwarn 3'
    f3.write(towrite)
    f3.close()
    time.sleep(2)

def rerun(norerun):
    copyfile('./go.sh', './rerun.sh')
    time.sleep(2)
    f3 = open('./rerun.sh', 'a+')
    if norerun < 4:
        towrite='mpirun -np 2 gmx_mpi grompp -f nvt2.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p complex2.top -o nvt.tpr -maxwarn 3'
    if norerun >= 4:
        towrite='mpirun -np 2 gmx_mpi grompp -f nvt3.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p complex2.top -o nvt.tpr -maxwarn 3'
    f3.write(towrite)
    f3.close()
    fN=open('./N.txt','a')
    fN.write(str(norerun))
    fN.write('\n')
    fN.close()

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
        tran_z=min_d-2.000        # z1 needs to fix to be large
        noatom=int(column2)
    return tran_z,noatom,column0  #noatom is how many atoms are there, coumnzero is the last name of the 1st column

                
def createvelocityandfile(filepath,tran_z,noatom,column0,T):
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
                        mynum=column0.replace('LS12','')
                        mynum=int(mynum)+1
                    firstcolumn=str(mynum)+'LS12'
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
                # print(towritefirst+towritea+towritenoa+towritep+towrites)

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
    print(x[minz_index], y[minz_index],minz)
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
        mind=float(min(d))
        fN=open('./N.txt','a')
        fN.write(str(mind))
        fN.write('\n')
        fN.close()
    return mind<0.4

def checkerror():
    with open('./gromacs.err','r') as f10:
        for line in (f10.readlines()):
            if 'Fatal error:' in line:
                return True
            else:
                return False
    f10.close()

T=300
new_z=1
myzv=0
zlimit=2.0
goterror=False
fN=open('./N.txt','w')
fN.close()
filepath='./LS12_box.gro'  #molecule you want to insert
for i in range(725):
    i=i+1
    while new_z<zlimit:
        createnewmolecule()
        subprocess.run(['sbatch', './insert.sh'])
        done=check_run_status()
        x1,y1,z1,noatom_insert=findminz(filepath)
        tran_z,noatom,column0=find_translation(i,x1,y1,z1)
        while myzv>=0:
            new_z,myzv=createvelocityandfile(filepath,tran_z,noatom,column0,T)
        myzv=0
        done=check_run_status()
        time.sleep(5)
    while goterror==True:
        createnewmolecule()
        subprocess.run(['sbatch', './insert.sh'])
        done=check_run_status()
        x1,y1,z1,noatom_insert=findminz(filepath)
        tran_z,noatom,column0=find_translation(i,x1,y1,z1)
        while myzv>=0:
            new_z,myzv=createvelocityandfile(filepath,tran_z,noatom,column0,T)
        myzv=0
        done=check_run_status()
        time.sleep(5)
        currentnoofatom=cretefinalfile(i,noatom_insert,filepath)
        top(currentnoofatom)
        time.sleep(5)
        compile()
        subprocess.run(['sbatch', './compile.sh'])
        time.sleep(5)
        done=check_run_status()
        time.sleep(5)
    createnewmolecule()
    subprocess.run(['sbatch', './insert.sh'])
    done=check_run_status()
    x1,y1,z1,noatom_insert=findminz(filepath)
    tran_z,noatom,column0=find_translation(i,x1,y1,z1)
    while myzv>=0:
        new_z,myzv=createvelocityandfile(filepath,tran_z,noatom,column0,T)
    myzv=0
    done=check_run_status()
    time.sleep(5)
    currentnoofatom=cretefinalfile(i,noatom_insert,filepath)
    top(currentnoofatom)
    time.sleep(5)
    compile()
    subprocess.run(['sbatch', './compile.sh'])
    time.sleep(5)
    done=check_run_status()
    time.sleep(5)
    if i%100!=0:
        subprocess.run(['sbatch', './test.sh'])
    if i%100==0:
        subprocess.run(['sbatch', './test2.sh'])
    done=check_run_status()
    goterror=checkerror()
    time.sleep(20)
    x1,y1,z1=findxyzlastmolecule('./nvt.gro',54)  #size of molecule
    mind=hasthemoleculedock('./nvt.gro',x1,y1,z1,54)
    norerun=0
    z1=float(z1)
    if z1 < zlimit: 
        subprocess.run(['sbatch', './test.sh'])
        done=check_run_status()
        goterror=checkerror()
        time.sleep(20)
        x1,y1,z1=findxyzlastmolecule('./nvt.gro',54)  #size of molecule
        mind=hasthemoleculedock('./nvt.gro',x1,y1,z1,54)
    while mind==False:
        norerun +=1
        rerun(norerun)
        subprocess.run(['sbatch', './rerun.sh'])
        done=check_run_status()
        time.sleep(5)
        subprocess.run(['sbatch', './test.sh'])
        done=check_run_status()
        time.sleep(20)
        x1,y1,z1=findxyzlastmolecule('./nvt.gro',54) #size of molecule
        mind=hasthemoleculedock('./nvt.gro',x1,y1,z1,54) #size of molecule
        if norerun > 5:
            mind=True
        
