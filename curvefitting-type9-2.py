# -*- coding: utf-8 -*-
"""
Created on Mon May 17 11:03:04 2021
Gromac torsional angle forecefield fitting-type 9
@author: user
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
xdata=[]
ydata=[]
filepath='E:/mCBD-1.txt'
with open(filepath,'r') as f:
    for i,line in enumerate(f):
        x=float(line.split()[0])*3.142/180
        y=float(line.split()[1])*2600  # conversion au to KJ/mol
        xdata.append(x)
        ydata.append(y)
xdata=np.asarray(xdata)
ydata=np.asarray(ydata)
sigma=ydata*0.01+0.1 # weighted fitting
def func(angle,k1,k2,k3,k4):  # defination of a function
    n1=2
    n2=2
    n3=4
    n4=6
    t1=0
    t2=3.142
    t3=0
    t4=0
    V=k1*(np.cos(n1*angle-t1)+1)+k2*(np.cos(n2*angle-t2)+1)+k3*(np.cos(n3*angle-t3)+1)+k4*(np.cos(n4*angle-t4)+1)
    return V

def drawgraph(func,x,y, p0):
    popt, pcov = curve_fit(func, x, y,p0, sigma=sigma,absolute_sigma=True,maxfev= 100000)                                                             
    predicted=func(x, *popt) 
    r=np.corrcoef(y, predicted)
    r2=r[0][1]**2
    print('coefficient of determination:', r2)
    ii=1
    for i in popt:
        print(i," ", ii ,"parameter")
        ii+=1   
    return popt, r2

plt.scatter(xdata,ydata ,color='blue', label='QM simulation')       
newx=np.linspace(0,3.142*2,100)
# plt.scatter(newx, func(newx, -1.239,1.243,2.741,0.4828),color='red',label='paper') 

popt, r2=drawgraph(func,xdata,ydata, p0=[-1.239,1.243,2.741,0.4828])

plt.scatter(newx, func(newx, *popt),color='orange',label='best fit') 

plt.xlabel('dihedral angle (rad)')  
plt.ylabel('KJ per mol')
plt.legend()
