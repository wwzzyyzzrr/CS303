import os

a = open("train_data.txt")
b = a.readlines()
r = input("Rate: ")
d = int(float(r)*len(b))
temp = ''
f = open('test.txt','w')
for i in range(0,d):
    c = b[i].split(' ')
    for j in range(len(c)-1):
        temp+=str(c[j])+' '
    temp+=c[len(c)-1]
print(temp, end = '', file = f)
temp = ''
f = open('test0.txt','w')
for i in range(d,len(b)):
    c = b[i].split(' ')
    for j in range(len(c)-1):
        temp+=str(c[j])+' '
    temp+=c[len(c)-1]   
print(temp, end = '', file = f)
for i in range(10):
    os.system("python3 SVM_GD.py")
    os.system("python3 SVM_GD_test.py")
