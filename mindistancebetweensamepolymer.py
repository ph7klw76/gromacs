iimport numpy as np

def dist(x1,y1,z1,x2,y2,z2):
    dis=np.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    return dis

def extract(a,m,molecule):
    data=[]
    for line in a:
        line=line.split()
        if molecule==line[0]:
            if line[1] in m:
                molecule2,atom_index,x2,y2,z2,element=line[0],int(line[2]),float(line[3]),float(line[4]),float(line[5]),line[1]
                data.append([molecule2,atom_index,x2,y2,z2,element])
    return data

d, data2, pair_info=[],[],[]
f=open('E:/npt.gro', 'r')
a=f.readlines()
m=['N1','N2','N3','N4','N5','N6','N7','N8', 'N9','N10','N11','N12']
resid='H1FV'
n=255 # number of residue +1
f2=open('E:/Se-pair.txt','w')
for i in range(1,n,1):
    molecule1=str(i)+resid
    data1=extract(a,m,molecule1)
    for ii in range(1,n,1):
        if i!=ii:
            molecule2=str(ii)+resid
            data2=extract(a,m,molecule2)
        if data2!=[]:
            for n1 in range(len(data1)):
                molecule1,atom_index1,x1,y1,z1,element1=data1[n1][0],data1[n1][1],data1[n1][2],data1[n1][3],data1[n1][4],data1[n1][5]
                for n2 in range(len(data2)):
                    molecule2,atom_index2,x2,y2,z2,element2=data2[n2][0],data2[n2][1],data2[n2][2],data2[n2][3],data2[n2][4],data2[n2][5]
                    distance=dist(x1,y1,z1,x2,y2,z2)
                    d.append(distance)
                    pair_info.append([molecule1,element1,molecule2,element2])
            print(min(d),pair_info[d.index(min(d))], sep=',',file=f2)   
            print(min(d),pair_info[d.index(min(d))])
            data2,d,pair_info=[],[],[]
f.close()
f2.close()
