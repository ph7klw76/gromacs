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

dopant_itp='E:/PHT/dopant.txt'
polymer_itp='E:/PHT/polymer.txt'        
residue_extract_1='P7F6'
residue_extract_2='U9EL'  #
ff_dopant='E:/PHT/'+residue_extract_1+'.txt'  #
ff_polymer='E:/PHT/'+residue_extract_2+'.txt'  #
ff_dopant2='E:/PHT/'+residue_extract_1+'_2.txt'  #
ff_polymer2='E:/PHT/'+residue_extract_2+'_2.txt'  #
NPT='E:/PHT/npt.gro'   #

extract_relevant(ff_dopant,dopant_itp,NPT,residue_extract_1,'CAro')  #6
extract_relevant(ff_polymer,polymer_itp,NPT,residue_extract_2,'CAro','S')  #5
find_center(ff_dopant,residue_extract_1,ff_dopant2,6)
find_center(ff_polymer,residue_extract_2,ff_polymer2,5)
mydis,mya=[],[]
myfile=open(ff_polymer,'r')
myfile2=open("E:/PHT/min-dopant-P3HT-withS",'w')


file = open(ff_polymer, 'r')
line_count = 0
for line in file:
    if line != "\n":
        line_count += 1
file.close() 


f=open('E:/PHT/ring.txt','r')  #
flines=f.readlines()

file2 = open('E:/PHT/ring.txt', 'r')  #
line_count2 = 0
for line in file2:
    if line != "\n":
        line_count2 += 1
file2.close() 


for i, line_1 in enumerate(open(ff_dopant2,'r')):
    print(i+1)
    ii=0
    xyz1=line_1[i].split(',')  
    a1,x1,y1,z1=xyz1[0],xyz1[1],xyz1[2],xyz1[3].strip('\n')    
    for line_2 in myfile:
        if (i+1)%6!=0:
            a2,b2,c2,x2,y2,z2=extractxyz(line_2,residue_extract_2)
            dis=finddistance(x1,y1,z1,x2,y2,z2)
            mydis.append(dis)
            mya.append([a1,a2,b2])
        if (i+1)%6==0:
           a2,b2,c2,x2,y2,z2=extractxyz(line_2,residue_extract_2)
           dis=finddistance(x1,y1,z1,x2,y2,z2)
           mydis.append(dis)
           mya.append([a1,a2,b2]) 
           ii+=1
           if ii==line_count:
               dist=min(mydis)
               Sminloc=mya[mydis.index(dist)]
               for iii in range(line_count2):
                   if Sminloc[2] in flines[iii]:
                      extra= flines[iii]
               print(str(Sminloc[0])+','+str(Sminloc[1])+','+str(Sminloc[2])+','+str(dist)+','+str(extra))
               myfile2.write(str(Sminloc[0])+','+str(Sminloc[1])+','+str(Sminloc[2])+','+str(dist)+','+str(extra))
               mydis,mya=[],[]
    myfile.seek(0)
myfile.close()
myfile2.close()

    
