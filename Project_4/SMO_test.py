import numpy as np

def predict(w, x):
    return np.sign(np.dot(x,w.T))

path = "test0.txt"
#path = input("Please input the path of the file that need be test") or "test0.txt"
a = open(path)
b = a.readlines()
test = []
value = []
for i in range(len(b)):
    temp = b[i].split(' ')
    test.append(list(map(float,temp[0:len(temp)-1])))
    value.append(float(temp[len(temp)-1]))
path = "smoModel.txt"
#path = input("Please input the path of the model") or "smoModel.txt"
a = open(path)
b = a.readline()
temp = b.split(' ')
m = []
for i in range(len(temp)-1):
    m.append(float(temp[i]))
w = np.array([m])
mm = list(predict(w,np.array(test)))
wrong = 0
for i in range(0,len(mm)):
    if mm[i] != value[i]:
        wrong+=1
print('Wrong Rate is %f'%(wrong/len(mm)))