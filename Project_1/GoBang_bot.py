import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0


class AI(object):

    def __init__(self, chessboard_size, color, time_out):
        self.color = color
        self.chessboard_size = chessboard_size
        self.time_out = time_out
        self.candidate_list = []

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
                        y.append()#死四

                elif flag == 3:

                elif flag == 2:



    def go(self, chessboard):
        COLOR = COLOR_BLACK
        self.candidate_list.clear()
