# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 14:16:30 2021
finding nearest cluster given a molecule in gromac MD
@author: user
"""
import numpy as np


def finddistance(x1,y1,z1,x2,y2,z2):
    x1=float(x1)
    y1=float(y1)
    z1=float(z1)
    x2=float(x2)
    y2=float(y2)
    z2=float(z2)
    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def extract_a_molecule(file,listres,wheretostartfrom,molecule_index):
    with open(file,'r') as f2:
        molecule_index=str(molecule_index)
        x2=[]
        y2=[]
        z2=[]
        for i,line in enumerate(f2):
            if i==1:
                no=int(line)
            if i>1+int(wheretostartfrom):
                if i<no+2:
                    line=line.split()
                    column0=line[0]
                    for res in listres:
                        if res in column0:
                            column0=column0.replace(res,'')
                    if column0 in molecule_index:
                        if i<=10000:
                            x=line[3]  #x
                            y=line[4]  #y
                            z=line[5]  #z
                        if i>10000:
                            x=line[2]
                            y=line[3]
                            z=line[4]   
                        z2.append(z)
                        y2.append(y)
                        x2.append(x)
    f2.close()
    return x2,y2,z2

def finding_distance_between_2_pair(x11,y11,z11,x22,y22,z22):
    for i in range(len(x11)):
        x1=x11[i]
        y1=y11[i]
        z1=z11[i]
        d=[]
        for ii in range(len(x22)):
            x2=x22[ii]
            y2=y22[ii]
            z2=z22[ii]
            dis=finddistance(x1,y1,z1,x2,y2,z2)
            d.append(dis)
        distance=np.mean(d)
    return distance
           
def intermolecular_distance(file,listres,wheretostartfrom,first_molecule_index,last_molecule_index):
    listofdistance=[]
    listofpair=[]
    pair=[]
    for i in range(first_molecule_index,last_molecule_index+1,1):
        x11,y11,z11=extract_a_molecule(file, listres ,wheretostartfrom,i)
        d=[]
        for ii in range(first_molecule_index,last_molecule_index+1,1):
            if i!=ii:
                x22,y22,z22=extract_a_molecule(file, listres ,wheretostartfrom,ii)        
                dis=finding_distance_between_2_pair(x11,y11,z11,x22,y22,z22)
                d.append(dis)
                pair.append([i, ii, dis])
        distance=np.min(d)
        last_2_cluster=np.argpartition(np.array(d),1)[:1]
        indexofpair=last_2_cluster[0]
        print(pair[indexofpair])
        listofdistance.append(distance)
        listofpair.append(pair[indexofpair])
        pair=[]
    return listofdistance,listofpair
        
file='C:/Users/user/Documents/data simulation/gromac/LS12-complex/md_0_1.gro'
wheretostartfrom=2800
listres=['LS12']
first_molecule_index=1401
last_molecule_index=1500
        
listofdistance,listofpair=intermolecular_distance(file,listres,wheretostartfrom,first_molecule_index,last_molecule_index)    
print('intermolecular distance = ', np.mean(listofdistance))

np.savetxt('E:/pair.txt', listofpair)