file='0.gro'
ffw=open('E:/test/b.txt','w') 
fw=open('E:/test/'+file,'w') 
fw.write('mol in water'+'\n')
fw.write(' 76'+'\n')
ff=open('E:/frame.gro','r')  # change
for i,line in enumerate(ff):
    A=line.split(' ')[0]+'AANK' # change
    B=line.split(' ')[1]+'AANK'  # change
    file1=str((i)//76)+'.gro'
    if file!=file1:
       fw.write('  0.00000  0.00000  0.00000')
       ffw.write('gmx_mpi editconf -f '+file+' -o '+file.split('.')[0]+'.pdb'+'\n')
       fw.close()
       fw=open('E:/test/'+file1,'w')
       fw.write('mol in water'+'\n')
       fw.write(' 76'+'\n')
       file=file1
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
