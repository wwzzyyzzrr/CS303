import numpy as np

def predict(x, w):
    test = np.c_[np.ones((x.shape[0])), x]
    return np.sign(np.dot(test, w))

path = "test0.txt"#input("Please input the path of the file that need be test") or "test.txt"
a = open(path)
b = a.readlines()
test = []
value = []
for i in range(len(b)):
    temp = b[i].split(' ')
    test.append(list(map(float,temp[0:len(temp)-1])))
    value.append(float(temp[len(temp)-1]))
path = "GDModel.txt" #input("Please input the path of the model") or "GDModel.txt"
a = open(path)
b = a.readline()
temp = b.split(' ')
m = []
for i in range(len(temp)-1):
    m.append(float(temp[i]))
w = np.array(m)
mm = list(predict(np.array(test), w))
wrong = 0
for i in range(0,len(mm)):
    if mm[i] != value[i]:
        wrong+=1
print('Wrong Rate is %f'%(wrong/len(mm)))