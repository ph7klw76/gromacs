# finding the angle of dopant-polymer


import numpy as np

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

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

fdopant=open('E:/PHT/min-dopant-P3HT-withS','r')
npt=open('E:/PHT/npt - Copy.gro','r')
f=open('E:/PHT/ring.txt','r')  #
flines=f.readlines()
file2 = open('E:/PHT/ring.txt', 'r')  #
line_count2 = 0
for line in file2:
    if line != "\n":
        line_count2 += 1
file2.close() 
fw=open('E:/PHT/min-dopant-P3HT-withS-angle','w')
for i, line in enumerate(fdopant):
    line=line.split(',')
    dopant=line[0]
    polymer=line[1]
    distance=line[3]
    for line_2 in npt:
        try:
            a11,b11,c11,x11,y11,z11=extractxyz(line_2,'P7F6')
        except:
            a11,b11,c11,x11,y11,z11=extractxyz(line_2,'U9EL') #
        x11,y11,z11=float(x11),float(y11),float(z11)
        if a11==int(dopant):
            if b11=='C10':  #
              x0, y0, z0=  x11,y11,z11
            if b11=='C18':  #
              x1, y1, z1=  x11,y11,z11
            if b11=='C20':  #
              x2, y2, z2=  x11,y11,z11
    ux, uy, uz = u = [x1-x0, y1-y0, z1-z0]
    vx, vy, vz = v = [x2-x0, y2-y0, z2-z0]
    u_cross_v = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx]
    v1 = np.array(u_cross_v)
    npt.seek(0)
    for line_2 in npt:
        try:
            a11,b11,c11,x11,y11,z11=extractxyz(line_2,'P7F6')
        except:
            a11,b11,c11,x11,y11,z11=extractxyz(line_2,'U9EL') #
        x11,y11,z11=float(x11),float(y11),float(z11)
        if a11==int(polymer):
            if b11==line[4]:
                x0, y0, z0=  x11,y11,z11
            if b11==line[6]:
                x1, y1, z1=  x11,y11,z11               
            if b11==line[8].strip('\n'):
                x2, y2, z2=  x11,y11,z11
    ux, uy, uz = u = [x1-x0, y1-y0, z1-z0]
    vx, vy, vz = v = [x2-x0, y2-y0, z2-z0]
    u_cross_v = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx]
    v2 = np.array(u_cross_v)
    npt.seek(0)
    angle=angle_between(v1,v2)*180/np.pi
    print(angle)
    fw.write(str(distance)+','+str(angle)+'\n')
    
fw.close()
fdopant.close()
npt.close()
f.close()
