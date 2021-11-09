import math

class Points(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, no):
        x = self.x - no.x
        y = self.y - no.y
        z = self.z - no.z
        return Points(x, y, z)

    def dot(self, no):
        x = self.x * no.x
        y = self.y * no.y
        z = self.z * no.z
        return x + y + z

    def cross(self, no):
        x = self.y * no.z - self.z * no.y
        y = self.z * no.x - self.x * no.z
        z = self.x * no.y - self.y * no.x
        return Points(x, y, z)

    
    def absolute(self):
        return pow((self.x ** 2 + self.y ** 2 + self.z ** 2), 0.5)
# Points(30.14,45.76,60.37), Points(30.29,46.27,61.68), Points(31.5,46.16,62.38), Points(32.7,46.13,61.62)
def dihedral(a,b,c,d):
    x = (b - a).cross(c - b)
    y = (c - b).cross(d - c)
    angle = math.acos(x.dot(y) / (x.absolute() * y.absolute()))
    return angle

def finding_position(a):
    f2=open(file,'r')
    for ii, line2 in enumerate(f2):
        line2=line2.split()
        if len(line2)==10:
            if int(line2[1])==int(a):
                x=float(line2[5])
                y=float(line2[6])
                z=float(line2[7])
                break
    f2.close()
    return Points(x,y,z)

def define_dihedral(a,b,c,d):
    a=finding_position(a)
    b=finding_position(b)
    c=finding_position(c)
    d=finding_position(d)
    return a,b,c,d
  
#file='D:/DBT3/single_1.pdb'
#P1,P2,P3,P4=define_dihedral(30,29,28,14)
#angle1=dihedral(P1,P2,P3,P4)
