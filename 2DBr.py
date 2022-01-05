def formatthenumber(a,count=False):
    if count==False:
        a_string =format(a, ".3f")
        aligned_string = "{:>8}".format(a_string)
    if count==True:
        a_string =str(a)
        aligned_string = "{:>5}".format(a_string)
    return aligned_string
d=0.597
n=1
for i in range(21):
    x=i*d
    x=formatthenumber(x)
    for ii in range(21):
        y=ii*d
        y=formatthenumber(y)
        z=formatthenumber(0)
        c=formatthenumber(n,count=True)
        n=n+1
        coor="{:>8}".format('1BrB')+"{:>7}".format('Br1')+c+x+y+z
        print(coor)
    
