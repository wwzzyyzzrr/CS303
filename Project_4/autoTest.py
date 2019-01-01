import os

path = input("Please Input The Path of the RAW Data") or "train_data.txt"
a = open(path)
b = a.readlines()
r = input("Please input the rate of the training data(range(0:1)): ") or 0.9
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
type = input("Please input the algorithm you need to use: ") or ("GD")
times = input("Please input the repeat times: ") or 5
if type!="GD":
    for i in range(int(times)):
        os.system("python3 SMO.py")
        os.system("python3 SMO_test.py")
else:
    for i in range(int(times)):
        os.system("python3 SVM.py")
        os.system("python3 SVM_test.py")
