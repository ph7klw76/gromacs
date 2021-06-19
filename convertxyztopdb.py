# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 14:50:40 2021
updating gromac odb withterachem xyz
@author: user
"""

import linecache
import re

def replace(inputgromac,outputgromac,terachemxyz):
    gromacupdate=open(outputgromac,'w')
    for i, line in enumerate(open(inputgromac,'r')):
        print(line)
        if 'HETATM' in line:
            n=i-1
            line2=line.split()
            terachem = linecache.getline(terachemxyz, n).split()
            terachemx=round(float(terachem[1]),3)
            terachemy=round(float(terachem[2]),3)
            terachemz=round(float(terachem[3]),3)
            linex=str('{0:.3f}'.format(terachemx))
            liney=str('{0:.3f}'.format(terachemy))
            linez=str('{0:.3f}'.format(terachemz))
            line=re.sub(line2[5], linex, line)
            line=re.sub(line2[6], liney, line)
            line=re.sub(line2[7], linez, line)
            print(line)
        gromacupdate.write(line)
    gromacupdate.close()
    
terachemxyz='E:/AX.xyz'
inputgromac='E:/ACRX.pdb'
outputgromac='E:/update.pdb'
replace(inputgromac,outputgromac,terachemxyz)