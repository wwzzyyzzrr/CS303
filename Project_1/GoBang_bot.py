import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0


class AI(object):

    def __init__(self, chessboard_size, color, time_out):
        self.color = color
        self.chessboard_size = chessboard_size
        self.time_out = time_out
        self.candidate_list = np.zeros((self.chessboard_size,self.chessboard_size))
    def count(self, chessboard, a, b, j, k, COLOR):
        i = 0
        while (-1 < a + j < 15 and -1 < b + k < 15 and chessboard[a + j, b + k] == COLOR):
            i = i + 1
            a = a + j
            b = b + k
        if (-1 < a + j < 15 and -1 < b + k < 15 and chessboard[a + j, b + k] == COLOR_NONE):
            i = i * 2
        else:
            i = i * 2 - 1
        return i

    def calcute_value(self, chessboard, a, b, COLOR):
        x = []
        value = 0
        if chessboard[a, b] == 0:
            x.append(self.count(chessboard,a,b,1,1,COLOR))
            x.append(self.count(chessboard,a,b,-1,1,COLOR))
            x.append(self.count(chessboard,a,b,1,0,COLOR))
            x.append(self.count(chessboard,a,b,0,1,COLOR))
            x.append(self.count(chessboard,a,b,-1,-1,COLOR))
            x.append(self.count(chessboard,a,b,1,-1,COLOR))
            x.append(self.count(chessboard,a,b,-1,0,COLOR))
            x.append(self.count(chessboard,a,b,0,-1,COLOR))
            y = []
            for i in range(0,3):
                flag = x[i] + x[i+4]
                if flag > 6:
                    y.append(1)
                elif flag == 6:
                    if (x[i] * x[i + 4] < 0 or x[i] == x[i + 4] or (x[i] == 5 or x[i + 4] == 5)):
                        y.append(1)#五连
                    else:
                        y.append(2)#活四
                elif flag == 5:
                    y.append(3)#冲四
                elif flag == 4:
                    if (x[i]*x[i+4] < 0):
                        y.append(8)#死四
                    else:
                        y.append(4)#活三
                elif flag == 3:
                    y.append(5)#冲三
                elif flag == 2:
                    if(x[i] == x[i + 4] or x[i] * x[i + 4] < 0):
                        y.append(8)#死二死三
                    else:
                        y.append(6)#活二
                elif flag == 1:
                    y.append(7)#冲二
                else:
                    y.append(8)#死二等
            z = [0,0,0,0,0,0,0,0,0]
            if (y.__sizeof__()>0):
                for m in y:
                    z[m] = z[m]+1
                if z[1] > 0:
                    value = 30
                elif z[2] > 0:
                    value = 28
                elif z[3] > 1:#双冲四
                    value = 26
                elif (z[3] > 0 and z[4] > 0):#四三
                    value = 24
                elif z[4] > 1:#双三
                    value = 22
                elif z[3] > 0:#冲四
                    value = 20
                elif (z[4] > 0 and z[5] > 0):#活三+冲三
                    value = 18
                elif z[4] > 0:#活三
                    value = 16
                elif z[5] > 0:#冲三
                    value = 16 - 2 * z[5]
                else:
                    value = 2*(z[6]+z[7]+z[8])
        return value



    def go(self, chessboard):
        COLOR = COLOR_BLACK
        for a in range (0,self.chessboard_size):
            for b in range (0,self.chessboard_size):
                value = self.calcute_value(chessboard,a,b,COLOR)
                if value > self.candidate_list(a,b):
