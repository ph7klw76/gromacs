residue='57R4'
ff=open('E:/test2.txt','w')
for i in range(2):
    myfile=open('E:/P3TT3.txt','r')
 #   a=str(int(i+7))+residue
    deltaz=0.45*i
    for ii,line in enumerate(myfile):
        line=line.split()
        a=int(line[0].split(residue)[0])+i*224
        print(a)
        a=str(a)+residue
        if len(line)==5:
            b=line[1]
            b=b[:-5]
            c=int(line[1].split(b)[1])
            m=1
        if len(line)==6: 
            b=line[1]
            c=int(line[2])
            m=0
        if i>0:
            c=44352*i+c
            c=str(c)
        d=float(line[3-m])+4.7*i
        d=str('{0:.3f}'.format(d))
        e=float(line[4-m])
        e=str('{0:.3f}'.format(e))
        f=float(line[5-m])# +0.345*i
        f=float(f)
        f=str('{0:.3f}'.format(f))
        if int(c)<10000:
            txt='{:>9} {:>5} {:>4} {:>7} {:>7} {:>7}'.format(a,b,c,d,e,f)
        if int(c)>=10000:
            c=str(b)+str(c)
            txt='{:>9} {:>10} {:>7} {:>7} {:>7}'.format(a,c,d,e,f)
        ff.write(txt+'\n')
    myfile.close()
ff.close()
