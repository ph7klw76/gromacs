"extract individual molecules and dumnp it to a gro and preaper conversion into pdb in gromac"
resi='DJYB'
ff=open('C:/Users/user/Documents/woon/npt2convert.gro','r')  # change
fw=open('C:/Users/user/Documents/woon/file/1.gro','w')  
ffw=open('C:/Users/user/Documents/woon/file/b.txt','w') 
fw.write('mol in water'+'\n')
fw.write(' 110'+'\n')
for i,line in enumerate(ff):
    A=int(line.split(resi)[0]) # change
    line=line.split()
    a=line[0]
    myindex=((i//110)+1)
    if (i%110)==0:
        file=str(myindex)+'.gro'
        fw.write('  0.00000  0.00000  0.00000')
        print('close file '+str(i))
        ffw.write('gmx_mpi editconf -f '+file+' -o '+file.split('.')[0]+'.pdb'+'\n')
        fw.close()
        fw=open('C:/Users/user/Documents/woon/file/'+file,'w')
        print('start file '+str(i))
        fw.write('mol in water'+'\n')
        fw.write(' 110'+'\n')
    if ((i//110))==A-1:     
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
ffw.close()  
