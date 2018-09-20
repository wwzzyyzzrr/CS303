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
            for i in range(0,3):



    def go(self, chessboard):
        COLOR = COLOR_BLACK
        self.candidate_list.clear()
