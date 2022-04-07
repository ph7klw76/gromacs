residue='QF5V'
ff=open('E:/test.txt','w')
for i in range(21):
    myfile=open('E:/P3HT.txt','r')
    a=str(int(i+1))+residue
    deltaz=0.45*i
    for ii,line in enumerate(myfile):
        line=line.split()
        b=line[0]
        c=int(line[1])
        if i>0:
            c=252*i+c
            c=str(c)
        d=line[2]
        e=line[3]
        f=line[4]
        f=float(f)+deltaz
        f=str('{0:.3f}'.format(f))
        txt='{:>9} {:>5} {:>4} {:>7} {:>7} {:>7}'.format(a,b,c,d,e,f)
        ff.write(txt+'\n')
    myfile.close()
ff.close()
