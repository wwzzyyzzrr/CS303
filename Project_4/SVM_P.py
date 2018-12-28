import numpy as np

class SVM:
    def __init__(self, x, y):
        self.x = np.c_[np.ones((x.shape[0])),x]
        self.y = y
        self.epochs = 1000
        self.learning_rate = 0.01
        self.w = np.random.uniform(size = np.shape(self.x)[1],)
    
    def get_loss(self, x, y):
        return max(0,1 - y * np.dot(x,self.w))
        
    def cal_sgd(self,x,y,w):
        if y*np.dot(x,w) < 1:
            w = w + self.learning_rate*(y*x)
        return w
    
    def train(self):
        for epoch in range(self.epochs):
            randomize = np.arange(len(self.x))
            np.random.shuffle(randomize)
            x = self.x[randomize]
            y = self.y[randomize]
            loss = 0
            for xi, yi in zip(x,y):
                loss += self.get_loss(xi,yi)
                self.w = self.cal_sgd(xi,yi,self.w)

def predict(x, w):
    test = np.c_[np.ones((x.shape[0])), x]
    return np.sign(np.dot(test, w))

def main():
    a = open("test.txt")
    b = a.readlines()
    matrix = []
    value = []
    d = 0.9
    for i in range(0, int(len(b)*d)):
        temp = b[i].split(' ')
        matrix.append(list(map(float,temp[0:len(temp)-1])))
        value.append(float(temp[len(temp)-1]))
    svm = SVM(np.array(matrix), np.array(value))
    #print(len(np.array(value)))
    svm.train()
    print(svm.w)
    a = open("test.txt")
    b = a.readlines()
    test = []
    value = []
    for i in range(int(len(b)*d),len(b)):
        temp = b[i].split(' ')
        test.append(list(map(float,temp[0:len(temp)-1])))
        value.append(float(temp[len(temp)-1]))
    mm = list(predict(np.array(test), svm.w))
    wrong = 0
    for i in range(0,len(mm)):
        if mm[i] != value[i]:
            wrong+=1
    print(wrong/len(b))

main()