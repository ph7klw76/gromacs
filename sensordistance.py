import numpy as np
resi='TTU7'
myfile=open('F:/sensor2/out.gro','r') # change
myfile=myfile.readlines()
myfile2=open('F:/sensor2/NO.txt','r') # change
myfile3=open('F:/sensor2/distance.txt','w') # change
mydistance=[]

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

for i,line1 in enumerate(myfile2):
    n=i+1
    line1=line1.split()
    a1=line1[0]
    if len(line1)==8:
        b1=line1[1]
        b1=b1[:-5]
        c1=int(line1[1].split(b1)[1])
        m1=1
    if len(line1)==9: 
        b1=line1[1]
        c1=int(line1[2])
        m1=0
    if len(line1)==9 or len(line1)==8:
        a1=a1.split(resi)[0]
        d1=float(line1[3-m1])
        e1=float(line1[4-m1])
        f1=float(line1[5-m1])
    for line in myfile:
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
            a=a.split(resi)[0]
            d=float(line[3-m])
            e=float(line[4-m])
            f=float(line[5-m])
        NOd=finddistance(d1,e1,f1,d,e,f)
        mydistance.append([NOd ,a1, a])
    if n%2==0:
        mydistance1=sorted(mydistance)[0]
        print(mydistance1)
        myfile3.write(str(mydistance1)+'\n')
        mydistance=[]
myfile2.close()
myfile3.close()
