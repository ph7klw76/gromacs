convert=open('E:/PHT/polymer-polymer/convert.txt','w')
ff=open('E:/PHT/polymer-polymer.txt','r')  # change
for i,line0 in enumerate(ff):
    print(line0)
    A=line0.split(',')[0]+'U9EL' # change
    B=line0.split(',')[1]+'U9EL'  # change
    fw=open('E:/PHT/polymer-polymer/'+A+'_'+B+'.gro','w')
    convert.write('gmx_mpi editconf -f '+A+'_'+B+'.gro'+' -o '+A+'_'+B+'.gro -pbc yes'+'\n')
    fw.write('extracted molecule'+'\n')  # total number of molecule, change
    fw.write('144'+'\n')
    myfile=open('E:/PHT/npt.gro','r') # change
    for ii,line in enumerate(myfile):
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
            d=float(line[3-m])
            e=float(line[4-m])
            f=float(line[5-m])
            b=b[0]
            if line[0]==A or line[0]==B:
                d=str('{0:.3f}'.format(d))
                e=str('{0:.3f}'.format(e))
                f=str('{0:.3f}'.format(f))
                if int(c)<10000:
                    txt='{:>9} {:>5} {:>4} {:>7} {:>7} {:>7}'.format(a,b,c,d,e,f)
                if int(c)>=10000:
                    c=str(b)+str(c)
                    txt='{:>9} {:>10} {:>7} {:>7} {:>7}'.format(a,c,d,e,f)
                fw.write(txt+'\n')
    fw.close()
convert.close()
