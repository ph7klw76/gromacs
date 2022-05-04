import numpy as np
from operator import itemgetter
ff=open('E:/P3HT-dopant.txt','w')

def finddistance(x1,y1,z1,x2,y2,z2):
    x1,y1,z1,x2,y2,z2=float(x1),float(y1),float(z1),float(x2),float(y2),float(z2)
    p1 = np.array([x1, y1, z1])
    p2 = np.array([x2, y2, z2])
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def extractxyz(line,residue):
    line=line.lstrip()
    line=line.split()
    a=int(line[0].split(residue)[0])
    if len(line)==8:
        b=line[1]
        b=b[:-5]
        c=int(line[1].split(b)[1])
        m=1
    if len(line)==9: 
        b=line[1]
        c=int(line[2])
        m=0
    d=float(line[3-m])
    e=float(line[4-m])
    f=float(line[5-m])
    return a,b,c,d,e,f
        
residue_extract='P7F6'
residue_extract_2='ZBZ8'
residue_1=open('E:/'+residue_extract+'.txt','w')
myfile=open('E:/npt0.gro','r')
for line in myfile:
    line_s=line.split()
    res_match=line_s[0][-4:]
    if residue_extract==res_match:
        residue_1.write(line.lstrip())
residue_1.close()

residue_read=open('E:/'+residue_extract+'.txt','r')
coor,S,loc=[],[],[]
for i,line_1 in enumerate(residue_read):
    print(i)
    a1,b1,c1,d1,e1,f1=extractxyz(line_1,residue_extract)
    if i==0:
        aa=a1
    if a1==aa:
        coor.append((d1,e1,f1))
    if a1!=aa:  
        myfile.seek(0)
        for line_2 in myfile:
            line_x=line_2.lstrip()
            line_x=line_2.split()
            if len(line_x)>=8:
                match=line_x[0][-4:]
                if residue_extract_2==match: #find polymer
                    a2,b2,c2,d2,e2,f2=extractxyz(line_2,residue_extract_2)#polymer
                    if b2[0]=='S':  # only look at S
                        for xyz in coor:
                            d=finddistance(xyz[0],xyz[1],xyz[2],d2,e2,f2)
                            S.append(d)
                            loc.append(a2)
        dist=min(S)
        Sminloc=loc[S.index(dist)]
        ff.write(str(a1)+','+str(Sminloc)+','+str(dist)+'\n')
        coor,S,loc=[],[],[]
        a1==aa
        coor.append((d1,e1,f1))
