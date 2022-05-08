import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def func(x,s,u,c):  # defination of a function
    a=(1/(s*np.sqrt(2*np.pi)))
    b=(x-u)/s
    g=a*np.exp(-0.5*b**2)
    return g*c

def drawgraph(func,x,y):
    popt, pcov = curve_fit(func, x, y)                                                             
    predicted=func(x, *popt) 
    r=np.corrcoef(y, predicted)
    r2=r[0][1]**2
    print('coefficient of determination:', r2)
    ii=1
    for i in popt:
        print(i," ", ii ,"parameter")
        ii+=1   
    return popt, r2

xdata=[]
ydata=[]
filepath='E:/P3TT/gaussian.txt'
with open(filepath,'r') as f:
    for i,line in enumerate(f):
        x=float(line.split()[0])
        y=float(line.split()[1]) # conversion eV to KJ/mol
        xdata.append(x)
        ydata.append(y)
xdata=np.asarray(xdata)
ydata=np.asarray(ydata)

fig, ax = plt.subplots(figsize=(12, 6))

    
plt.scatter(xdata,ydata)       
newx=np.linspace(0.25,0.55,100)

popt, r2=drawgraph(func,xdata,ydata)

plt.plot(newx, func(newx, *popt),color='orange',label='best fit') 
f=open('E:/P3TT/gaussian2.txt','w')
yy=func(newx, *popt)
for xx in newx:
    f.write(str(xx)+','+str(yy[0])+'\n')
f.close()
