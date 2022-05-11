# extracting polymer cluster arround a dopant=polymer pair

import numpy as np

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

def extract_relevant(file_w,file_r_itp,NTP,residue,itp1,itp2='None',itp3='None',itp4='None',itp5='None'): # match the aromatic ring
    dopant_res=[]
    file1=open(file_r_itp,'r') 
    for i, dopant in enumerate(file1):
        res0=dopant.split()[0]
        res1=dopant.split()[1]
        if res0==itp1:
            dopant_res.append(res1)
        if res0==itp2:
            dopant_res.append(res1)
        if res0==itp3:
            dopant_res.append(res1)
        if res0==itp4:
            dopant_res.append(res1)
        if res0==itp5:
            dopant_res.append(res1)
    file1.close()
    file2=open(NPT,'r')
    file3=open(file_w,'w')     
    for line in file2:
        line_s=line.split()
        res_match=line_s[0][-4:]
        if residue==res_match:
            a,b,c,d,e,f=extractxyz(line,residue)
            if b in dopant_res:
                file3.write(line.lstrip())
    file1.close()
    file2.close()
    file3.close()
    return 

def find_center(ff_dp,residue,ff1,number):
    d1,e1,f1=[],[],[]
    number=int(number)
    ff=open(ff1,'w')
    fff=open(ff_dp,'r')
    for i,line in enumerate(fff): #6
        if (i+1)%number!=0:
            a,b,c,d,e,f=extractxyz(line,residue)
            d1.append(float(d))
            e1.append(float(e))
            f1.append(float(f))
        if (i+1)%number==0:
            a,b,c,d,e,f=extractxyz(line,residue)
            d1.append(float(d))
            e1.append(float(e))
            f1.append(float(f))
            ff.write(str(a)+','+str(np.average(d1))+','+str(np.average(e1))+','+str(np.average(f1))+'\n')
            d1,e1,f1=[],[],[]
    ff.close()
    fff.close()
    return

def find_location(mya,mydis,iii):
    s=sorted(mydis)
    while True:
        p1=mya[mydis.index(s[iii])][1]
        p2=mya[mydis.index(s[iii+1])][1]
        iii+=1
        if p1!=p2:
           d=s[iii]
           break
    return p2,iii

dopant_itp='E:/PHT/dopant.txt'
polymer_itp='E:/PHT/polymer.txt'        
residue_extract_1='P7F6'
residue_extract_2='U9EL'  #
ff_dopant='E:/PHT/'+residue_extract_1+'.txt'  #
ff_polymer='E:/PHT/'+residue_extract_2+'.txt'  #
ff_dopant2='E:/PHT/'+residue_extract_1+'_2.txt'  #
ff_polymer2='E:/PHT/'+residue_extract_2+'_2.txt'  #
NPT='E:/PHT/npt - Copy.gro'   #

# extract_relevant(ff_dopant,dopant_itp,NPT,residue_extract_1,'CAro')  #6
# extract_relevant(ff_polymer,polymer_itp,NPT,residue_extract_2,'CAro','S')  #5
# find_center(ff_dopant,residue_extract_1,ff_dopant2,6)
# find_center(ff_polymer,residue_extract_2,ff_polymer2,5)
mydis,mya=[],[]
myfile=open(NPT,'r')
myfile2=open("E:/PHT/dopant-polymer-cluster.txt",'w')



f=open(ff_dopant2,'r')  #
flines=f.readlines()

file2 = open(NPT, 'r')  #
line_count2 = 0
for line in file2:
    if line != "\n":
        line_count2 += 1
file2.close() 

polymercluster=[]
for i, line_1 in enumerate(open('E:/P3TT/min-dopant-P3TT-withS.txt','r')):
    xyz1=line_1.split(',')  
    dopant1=int(xyz1[0])
    polymer1=int(xyz1[1])
    polymercluster.append(polymer1)
    min_d=xyz1[3]
    line_2=flines[i].split(',')
    x1,y1,z1=line_2[1],line_2[2],line_2[3] 
    print('dopant=',i)      
    ii=1
    for line_3 in myfile:
        a2,b2,c2,x2,y2,z2=extractxyz(line_3,residue_extract_2)
        dis=finddistance(x1,y1,z1,x2,y2,z2)
        mydis.append(dis)
        mya.append([dopant1,a2])
        ii+=1
        if ii==line_count2:
            p2,iii=find_location(mya,mydis,1)
            for x in range(5):
                while p2 in polymercluster:
                    p2,iii=find_location(mya,mydis,iii)
                polymercluster.append(p2)
            for xx in range(len(polymercluster)):
                myfile2.write(str(polymercluster[xx])+',')
                print(polymercluster[xx])
            myfile2.write('\n')
            mydis,mya,polymercluster=[],[],[]
    myfile.seek(0)
myfile.close()
myfile2.close()
