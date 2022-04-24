residue='0EKF'
ff=open('E:/test2.txt','w')
for i in range(14):
    myfile=open('E:/P3TT.txt','r')
 #   a=str(int(i+7))+residue
    deltaz=0.45*i
    for ii,line in enumerate(myfile):
        line=line.split()
        a=int(line[0].split(residue)[0])+i*7
        a=str(a)+residue
        b=line[1]
        c=int(line[2])
        if i>0:
            c=1736*i+c
            c=str(c)
        d=float(line[3])
        d=str('{0:.3f}'.format(d))
        e=float(line[4])
        e=str('{0:.3f}'.format(e))
        f=float(line[5])
        f=float(f)+0.65*i
        f=str('{0:.3f}'.format(f))
        if int(c)<10000:
            txt='{:>9} {:>5} {:>4} {:>7} {:>7} {:>7}'.format(a,b,c,d,e,f)
        if int(c)>=10000:
            c=b+c
            txt='{:>9} {:>10} {:>7} {:>7} {:>7}'.format(a,c,d,e,f)
        ff.write(txt+'\n')
    myfile.close()
ff.close()
