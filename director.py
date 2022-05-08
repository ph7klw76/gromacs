import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random as rd
wf=open('E:/P3HT/director_dist.txt','w')
mydataset = open('E:/P3HT/ZBZ8_2.txt','r')
a,x,y,z,angle0,S0=[],[],[],[],[],[]
for i,line in enumerate(mydataset):
    line=line.split(',')
    a=int(line[0])
    if (i+1)%10!=0:
        x.append(float(line[1]))
        y.append(float(line[2]))
        z.append(float(line[3].strip('\n')))
    if (i+1)%10==0:
        x.append(float(line[1]))
        y.append(float(line[2]))
        z.append(float(line[3].strip('\n')))
        coords = np.array((x, y, z)).T
        pca = PCA(n_components=1)
        pca.fit(coords)
        direction_vector = pca.components_
        # print(direction_vector)
        vector_1 =[1,0,0]
        vector_2 =[direction_vector[0][0],direction_vector[0][1],direction_vector[0][2]]
        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle = np.arccos(dot_product)
        S=(3*np.cos(angle)*np.cos(angle)-1)/2
        S0.append(S)
        angle0.append((angle/np.pi)*180)
        x,y,z=[],[],[]
bins=[i*10 for i in range(19)]
aa,bb,cc=plt.hist(angle0,bins, density = True)
plt.show()
print(np.mean(S0))
for i in range(18):
    wf.write(str(5+i*10)+','+str(aa[i])+'\n')
    i+=1
wf.write(str(np.mean(S0)))
wf.close()
