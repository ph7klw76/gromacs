import numpy as np
import matplotlib.pyplot as plt

def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)

def countline(file):
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    return  line_count 

a = np.mgrid[:100, :100, :100][0]
for i in range(len(a)):
    a[i]=0

def generate_volume(filepath):
    file=open(filepath,'r')    
    flines=file.readlines()
    count=countline(flines)     
    for i in range(count):
        fline=flines[i].split(',')
        x,y,z=fline[1],fline[2],fline[3].strip('\n')
        x,y,z=round(float(x),1),round(float(y),1),round(float(z),1)
        x,y,z=int(x*10),int(y*10),int(z*10)
        for xi in range(x-1,x+2):
            for yi in range(y-1,y+2):
                for zi in range(z-1,z+2):
                    if -1<z<99 and -1<yi<99 and -1<xi<99:
                        a[xi][yi][zi]=1
    return a

filepath= 'E:/P3HT/P7F6volume_2.txt'
filepath2= 'E:/P3TT/P7F6volume_2.txt'
filepath3= 'E:/PHT/P7F6volume_2.txt'
a=generate_volume(filepath)
a2=generate_volume(filepath2)
a3=generate_volume(filepath3)


S=np.fft.fftn(a)
S2=np.fft.fftn(a2)
S3=np.fft.fftn(a3)
Slog=np.log(np.abs(S))
Slog2=np.log(np.abs(S2))
Slog3=np.log(np.abs(S3))

def transform_xyz(S):
    x,y,z,Value=[],[],[],[]
    N=len(S)
    for xi in range(N):
        for yi in range(N):
            for zi in range(N):
                x.append((xi-50)/10)
                y.append((yi-50)/10)
                z.append((zi-50)/10)
                Value.append(abs(S[xi][yi][zi]))
    return x,y,z,Value

x,y,z,Value=transform_xyz(Slog)
x2,y2,z2,Value=transform_xyz(Slog2) 
x3,y3,z3,Value=transform_xyz(Slog3)   
          
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax= fig.add_subplot(projection='3d')
 
p=ax.scatter3D(x,y,z, c=Value, lw=0, s=20, label='F4TCNQ in P3HT')
fig.colorbar(p)
ax.set_xlabel('X-spatial frequency (nm{})'.format(get_super('-1')))
ax.set_ylabel('Y-spatial frequency (nm{})'.format(get_super('-1')))
ax.set_zlabel('Z-spatial frequency (nm{})'.format(get_super('-1')))
plt.show() 
