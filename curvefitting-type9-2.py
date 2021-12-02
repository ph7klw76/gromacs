import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
xdata=[]
ydata=[]
filepath='D:/DBT1-1-2.txt'
with open(filepath,'r') as f:
    for i,line in enumerate(f):
        x=float(line.split()[0])
        y=float(line.split()[1])*96.486  # conversion eV to KJ/mol
        xdata.append(x)
        ydata.append(y)
xdata=np.asarray(xdata)
ydata=np.asarray(ydata)
sigma=ydata*0.01+0.1 # weighted fitting
def func(angle,k1,k2,k3,k4):  # defination of a function
    n1=2
    n2=1
    n3=1
    n4=0
    t1=0
    t2=3.142/2
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

fig, ax = plt.subplots(figsize=(12, 6))

for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	label.set_fontsize(16)
    
plt.scatter(xdata,ydata ,color='blue', label='DFT/LC-*wpbeh/def2svp')       
newx=np.linspace(-1,3.5,100)
# plt.scatter(newx, func(newx, -1.239,1.243,2.741,0.4828),color='red',label='paper') 

popt, r2=drawgraph(func,xdata,ydata, p0=[-1.239,1.243,2.741,0.4828])

plt.plot(newx, func(newx, *popt),color='orange',label='best fit') 

plt.xlabel('Torsional angle (rad)', fontsize=20)  
plt.ylabel('KJ per mol', fontsize=20)
plt.title('Torsional Potential of C37-N21-C22-C23',fontsize=20)
plt.legend( prop={"size":20})
