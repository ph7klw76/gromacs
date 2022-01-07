import numpy as np
import os

def extract_xyz(file,index):
    index=index+1
    f=open(file,'r')
    for i, line in enumerate(f):
        if i==index:
            line=line.split()
            z,y,x=line[-4],line[-5],line[-6]
            return float(x),float(y), float(z)
    f.close()

def finddistance(x1,y1,z1,x2,y2,z2):
    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def find_packing(file,result):  # full destination
    ff=open(result, 'w')
    molecule_A=np.array([2,3,4,6,7,8,10,12,13,15,16,17,19,37,38,40,42,43,44,45,47,49,51,53,54,55])  #atomic label (viewed in gaussian
    molecule_B=molecule_A+56
    mydata=np.zeros([len(molecule_A),len(molecule_B)])
    for i, indexA in enumerate(molecule_A):
        xA,yA,zA=extract_xyz(file,indexA)
        for ii, indexB in enumerate(molecule_B):
            xB,yB,zB=extract_xyz(file,indexB)
            mydata[i][ii]=finddistance(xA,yA,zA,xB,yB,zB)
    
    S1S1=mydata[0:3,0:3]  #row, column
    S1S2=mydata[3:6,0:3]
    S2S1=mydata[0:3,3:6]  #row, column
    S2S2=mydata[3:6,3:6]
    dis=np.array([np.trace(S1S1)/13,
                  np.trace(S1S2)/13,
                  np.trace(S2S1)/13,
                  np.trace(S2S2)/13])
    print(min(dis))
    if min(dis)<0.4:
        to_write0=file.split('/')[1]
        myindex=np.where(dis == dis.min())[0][0]
        ff.write(to_write0+'\n')
    ff.close()

result='./result_stacking.txt'
my_list = os.listdir('./')
for filename in my_list:
    if 'pair' in filename:
        entry_path = os.path.join('./', filename)
        if os.path.isdir(entry_path):
            file='./'+filename+'/'+filename+'.gro'
            find_packing(file,result)
