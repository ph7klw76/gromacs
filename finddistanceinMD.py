resi='DJYB'
myfile=open('C:/Users/user/Documents/woon/npt2.gro','r') # change
myfile2=open('C:/Users/user/Documents/woon/BS116d.txt','w') # change
mylist=['N4','N3','N2','N1','C14','C11']
for ii,line in enumerate(myfile):
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
    for item in mylist:
        if item==b:
            if len(line)==9 or len(line)==8:
                a=a.split(resi)[0]
                d=float(line[3-m])
                e=float(line[4-m])
                f=float(line[5-m])
                towrite=str(a)+','+str(d)+','+str(e)+','+str(f)+'\n'
                myfile2.write(towrite)
myfile.close()
myfile2.close()

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
thefilepath='C:/Users/user/Documents/woon/BS116d.txt'
count = len(open(thefilepath).readlines(  ))
myfile=open((thefilepath),'r') # change
for ii,line in enumerate(myfile):
    line=line.split(',')
    a,x1,y1,z1=int(line[0]),float(line[1]),float(line[2]),float(line[3])
    if ii==0:
        p1 = np.array([a,x1, y1, z1])
    if ii!=0:
        p2 = np.array([a,x1, y1, z1])
        p1 = np.vstack((p1,p2))
myi1,myi2=0,0
data1,data2=[],[]
thefilepath2='C:/Users/user/Documents/woon/BS116dd.txt'
myfile2=open((thefilepath2),'w') # change
for item1 in p1:
    for item2 in p1:
        if int(item1[0])!=int(item2[0]):
            x1,y1,z1=item1[1],item1[2],item1[3]
            x2,y2,z2=item2[1],item2[2],item2[3]
            dist=finddistance(x1,y1,z1,x2,y2,z2)
            data1.append(dist)
            myi1=myi1+1
            if myi1==6: # change
                dis=np.mean(data1)
                print(dis)
                print(str(item1[0])+','+str(item2[0]))
                myfile2.write(str(item1[0])+','+str(item2[0])+','+str(dis)+'\n')
                data1=[]
                myi1=0    
myfile2.close()

import numpy as np
mydata=[]
thefilepath2='C:/Users/user/Documents/woon/BS116dd.txt'
thefilepath3='C:/Users/user/Documents/woon/BS116ddd.txt'
myfile3=open((thefilepath3),'w') 
x=np.loadtxt(thefilepath2, delimiter=',')
ind=np.argsort(x[:,-1])
b=x[ind]
for i in range(5000):
    number0=b[i][1]
    number1=b[i][0]
    for ii in range(len(b)):
        if i!=ii:
            number00=b[ii][1]
            number11=b[ii][0]
            if number00==number0 and number11==number1:
                mydata.append(b[ii][2])
    d=np.mean(mydata)
    mydata=[]
    towrite=str(number0)+','+str(number1)+','+str(d)
    print(towrite)
    myfile3.write(towrite+'\n')
myfile3.close()
