class a:
    def __init__(self):
        mm = 0


x=[]
t = a()
t.mm = 1
x.append(t)
for i in range(1,5):
    x.append(a())
    x[i].mm = x[i-1].mm+i
for k in x:
    print k.mm
