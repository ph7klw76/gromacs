#EXTRACT OUT COORDINATE of RESI"
# resi='J8JX'
# myfile=open('E:/nvt.gro','r') # change
# myfile2=open('E:/dg7-mcbp.txt','w') # change
# mylist=['N4','N3','N2','N1','B1']
# for ii,line in enumerate(myfile):
#     line=line.split()
#     a=line[0]
#     if resi in a:
#         if len(line)==8:
#             b=line[1]
#             b=b[:-5]
#             c=int(line[1].split(b)[1])
#             m=1
#         if len(line)==9: 
#             b=line[1]
#             c=int(line[2])
#             m=0
#         for item in mylist:
#             if item==b:
#                 if len(line)==9 or len(line)==8:
#                     a=a.split(resi)[0]
#                     d=float(line[3-m])
#                     e=float(line[4-m])
#                     f=float(line[5-m])
#                     towrite=str(a)+','+str(d)+','+str(e)+','+str(f)+'\n'
#                     myfile2.write(towrite)
# myfile.close()
# myfile2.close()


resi='VZIF'
myfile=open('E:/nvt.gro','r') # change
myfile2=open('E:/dg7-mcbp2.txt','w') # change
mylist=['C2','C7','N1','C17','C14','C20','C23','N2','C34','C27']
for ii,line in enumerate(myfile):
    line=line.split()
    a=line[0]
    if resi in a:
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
a0=1
mydatad=[]
position=[]
myfile_1=open('E:/dg7-mcbp.txt','r') 
myfile_2=open('E:/dg7-mcbp2.txt','r') # change
myfile_3=myfile_2.readlines()
myfile_4=open('E:/dg7-mcbp-min.txt','w')
n=len(myfile_3)
for i,line in enumerate(myfile_1):
    axyz=line.split(',')
    a,x,y,z =int(axyz[0]),float(axyz[1]),float(axyz[2]),float(axyz[3].strip('\n'))
    if a0==a:
        for ii in range(n):
            axyz2=myfile_3[ii].split(',')
            aa,xx,yy,zz =int(axyz2[0]),float(axyz2[1]),float(axyz2[2]),float(axyz2[3].strip('\n'))
            d=finddistance(xx,yy,zz,x,y,z)
            mydatad.append(d)
            position.append([a,aa])
        a0=a
    if a0!=a: #new molecule
       location=position[mydatad.index(min(mydatad))]
       distance=min(mydatad)
       print(location,distance)
       myfile_4.write(str(location[0])+','+str(location[1])+','+str(distance)+'\n')
       mydatad=[]
       position=[]
       axyz2=myfile_3[ii].split(',')
       aa,xx,yy,zz =int(axyz2[0]),float(axyz2[1]),float(axyz2[2]),float(axyz2[3].strip('\n'))
       d=finddistance(xx,yy,zz,x,y,z)
       mydatad.append(d)
       position.append([a,aa])
