"""
extract a pair of molecule from gromacs and convert to xyz files

"""

ff=open('E:/P3HT-dopant.txt','r')
for i,line0 in enumerate(ff):
    A=line0[0]+'P7F6' # change
    B=line0[1]+'ZBZ8'  # change
    fw=open('E:/P3HT/'+A+'_'+B+'.xyz','w')
    fw.write('272'+'\n')  # total number of molecule, change
    fw.write('iiii'+'\n')
    line0=line0.split(',')
    myfile=open('E:/md1.gro','r') # change
    for ii,line in enumerate(myfile):
        line=line.split()
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
        b=b[0]
        txt='{:>4} {:>7} {:>7} {:>7}'.format(b,d,e,f)
        if line[0]==A or line[0]==B:
            fw.write(txt+'\n')
    fw.close()
