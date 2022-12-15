import numpy as np

def dist(x1,y1,z1,x2,y2,z2):
    dis=np.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    return dis

def extract(a_data,mm,molecule):
    data=[]
    for line in a_data:
        line=line.split()
        a=line[0]
        if len(line)==8:
            b=line[1]
            b=b[:-5]
            c=int(line[1].split(b)[1])
            m=1
        if len(line)==9: 
            b=line[1]
            c=int(line[2])
            m=0
        if len(line)==9 or len(line)==8:
            x=float(line[3-m])
            y=float(line[4-m])
            z=float(line[5-m])
            if molecule==a:
                if b in mm:
                    data.append([a,b,c,x,y,z])
    return data
d, data2, pair_info=[],[],[]
f=open('F:/nvt-longtest.gro', 'r')
a=f.readlines()
m=['N1','N2','N3','N4','N5','N6','N7','N8', 'N9','N10','N11','N12','S1','S2','S3','S4','S5','S6','S7','S8', 'S9','S10','S11','S12']
resid='QD81'
resid2='HHPA'
m2=['N1','N2','N3','C11','C12','C13','C14','C15','C16','C4','C5','C6','C7','C8']
n_1=259 # number of residue +1
n_2=260 #517
f2=open('F:/S-dopant.txt','w')
for i in range(n_1,n_2,1):
    molecule1=str(i)+resid2
    data1=extract(a,m2,molecule1)
    for ii in range(1,n_1,1):
        molecule2=str(ii)+resid
        data2=extract(a,m,molecule2)
        if data2!=[]:
            for n1 in range(len(data1)):   #one whole dopant
                molecule1,element1,index,x1,y1,z1=data1[n1][0],data1[n1][1],data1[n1][2],data1[n1][3],data1[n1][4],data1[n1][5]
                for n2 in range(len(data2)): #one whole polymer
                    molecule2,element2,index,x2,y2,z2=data2[n2][0],data2[n2][1],data2[n2][2],data2[n2][3],data2[n2][4],data2[n2][5]
                    distance=dist(x1,y1,z1,x2,y2,z2)
                    d.append(distance)
                    print(i,ii)
                    pair_info.append([molecule1,element1,molecule2,element2])
    print(min(d),pair_info[d.index(min(d))], sep=',',file=f2)   
    print(min(d),pair_info[d.index(min(d))])
    data2,d,pair_info=[],[],[]
f.close()
f2.close()

    
