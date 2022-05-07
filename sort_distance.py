import shutil
import os
ff=open('E:/PHT/polymer-polymer.txt','r')  # change
for i,line0 in enumerate(ff):
    A=line0.split(',')[0]+'U9EL' # change
    B=line0.split(',')[1]+'U9EL'  # change
    C=float(line0.split(',')[2].strip('\n'))
    source='E:/PHT/polymer-polymer/converted/'+A+'_'+B+'.gro'
    start=240
    end=420
    for i in range(start,end,10):
        if i/1000<C<i/1000+0.0025:
            path='E:/PHT/polymer-polymer/converted/'+str(i)
            if not os.path.exists(path):
                os.makedirs(path)
            destination=path+'/'+A+'_'+B+'.gro'
            shutil.copy(source, destination)
ff.close()
