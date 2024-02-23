import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
xdata=[]
ydata=[]
filepath='E:/DPPPz_scan.txt'
with open(filepath,'r') as f:
    for i,line in enumerate(f):
        x=float(line.split()[0])*np.pi/180 # convert to radiance
        y=float(line.split()[1])*4.18  # conversion eV to KJ/mol
        xdata.append(x)
        ydata.append(y)
xdata=np.asarray(xdata)
ydata=np.asarray(ydata)
sigma=ydata*0.01+0.1 # weighted fitting
def rb_potential(phi, C0, C1, C2, C3, C4, C5, C6):
    return (C0 + C1 * np.cos(phi) + C2 * np.cos(2*phi) + C3 * np.cos(3*phi) + 
            C4 * np.cos(4*phi) + C5 * np.cos(5*phi) + C6 * np.cos(6*phi))

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
newx=np.linspace(0,2*np.pi,100)
# plt.scatter(newx, func(newx, -1.239,1.243,2.741,0.4828),color='red',label='paper') 

popt, r2=drawgraph(rb_potential,xdata,ydata, p0=[-1.239,1.243,2.741,0.4828,2.741,0.4828,0.4828]) # seven guess value

plt.plot(newx, rb_potential(newx, *popt),color='orange',label='best fit') 

plt.xlabel('Torsional angle (rad)', fontsize=20)  
plt.ylabel('KJ per mol', fontsize=20)
plt.title('Torsional Potential of C37-N21-C22-C23',fontsize=20)
plt.legend( prop={"size":20})
