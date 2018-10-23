# -*- coding:utf-8 -*
import numpy as np
import random
import time
import copy

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0


class AI(object):

    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def count(self, chessboard, a, b, j, k, COLOR):
        i = 0
        m = 0
        flag = 0
        while (-1 < a + j < 15 and -1 < b + k < 15 and chessboard[a + j, b + k] != -COLOR):
            if chessboard[a + j, b + k] == COLOR:
                if flag == 0:
                    i = i + 1
                else:
                    m = m + 1
                a = a + j
                b = b + k
            elif -1 < a + 2 * j < 15 and -1 < b + 2 * k < 15:
                if chessboard[a + (2 * j), b + (2 * k)] == COLOR and flag == 0:
                    m = i
                    flag = 1
                    a = a + j
                    b = b + k
                else:
                    break
            else:
                break

        if (-1 < a + j < 15 and -1 < b + k < 15):
            if chessboard[a + j, b + k] == COLOR_NONE:
                i = i * 2
                m = m * 2
            else:
                m = m * 2 -1
                i = i * 2 - 1
        else:
            i = i * 2 - 1
            m = m * 2 - 1
        return [i,m]

    def calcute_value(self, chessboard, a, b, COLOR):
        x = []
        value = 0
        x.append(self.count(chessboard, a, b, 1, 1, COLOR))
        x.append(self.count(chessboard, a, b, -1, 1, COLOR))
        x.append(self.count(chessboard, a, b, 1, 0, COLOR))
        x.append(self.count(chessboard, a, b, 0, 1, COLOR))
        x.append(self.count(chessboard, a, b, -1, -1, COLOR))
        x.append(self.count(chessboard, a, b, 1, -1, COLOR))
        x.append(self.count(chessboard, a, b, -1, 0, COLOR))
        x.append(self.count(chessboard, a, b, 0, -1, COLOR))
        y = []
        for i in range(0, 4):
            flag = x[i][0] + x[i + 4][0]
            enough = 0
            if flag > 6:
                y.append(1)
                enough = 1
            elif flag == 6:
                enough = 1
                if (x[i][0] * x[i + 4][0] < 0 or x[i][0] == x[i + 4][0] or (x[i][0] == 5 or x[i + 4][0] == 5)):
                    y.append(1)  # 五连
                else:
                    y.append(2)  # 活四
            elif flag == 5:
                enough = 1
                y.append(3)  # 冲四
            elif flag == 4:
                if (x[i][0] * x[i + 4][0] < 0):
                    y.append(10)  # 死四
                else:
                    enough = 1
                    y.append(4)  # 活三
            elif flag == 3:
                y.append(5)  # 冲三
            elif flag == 2:
                if (x[i][0] == x[i + 4][0] or x[i][0] * x[i + 4][0] < 0):
                    y.append(10)  # 死二死三
                else:
                    y.append(6)  # 活二
            elif flag == 1:
                y.append(7)  # 冲二
            elif flag == 0:
                if (x[i][0] * x[i + 4][0]) == 0:
                    y.append(8)  # 活一
                else:
                    y.append(10)  # 死二
            elif flag == -1:
                y.append(9)  # 冲一

            if (x[i][1] > 5 or x[i+4][1] > 5):
                y.append(3)
            if (x[i][1]>3 and x[i+4][0]>1)or (x[i+4][1]>3 and x[i][0]>1):
                y.append(3)
            elif (x[i][0]>1 and x[i+4][1]>1) or (x[i][1]>1 and x[i+4][0]>1):
                y.append(4)
            elif (x[i][0]>=0 and x[i+4][1]>3) or (x[i][1]>3 and x[i+4][0]>=0):
                y.append(4)


           
        z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for m in y:
            z[m] = z[m] + 1
        if z[1] > 0:
            value = 100
        elif (z[2] > 0 and (z[3] > 0 or z[4] > 0)):
            value = 60 + z[3] * 6 + z[4] * 4
        elif z[2] > 0:
            value = 60
        elif z[3] + z[12]> 1 :  # 双冲四
            value = 56
        elif ((z[3]+z[12]> 0 )and z[4] > 0):  # 四三
            value = 52
        elif z[4] + z[11]> 1:  # 双三
            value = 48
        elif (z[4] > 0 and z[5] > 0):  # 活三+冲三
            value = 44
        elif z[3] + z[12]> 0:  # 冲四
            value = 40
        elif (z[4] > 0 and z[6] > 0):  # 活三 + 活二
            value = 36       
        elif z[4] > 0 :  # 活三
            value = 32
        elif z[5] > 0 :  # 冲三
            value = 28 + z[5]
        elif (z[5] > 0 and a[6] > 0):  # 冲三+活二
            value = 24
        elif z[6] > 0:  # 活二
            value = 20 + z[6]
        elif z[7] > 0:  # 冲二
            value = 16 + z[7]
        elif z[8] > 0:  # 活一
            value = 12 + z[8]
        elif z[9] > 0:
            value = z[9]
        else:
            value = 4
        return value

    def go(self, chessboard):
        candidate_value = np.array([[-2 for j in range(self.chessboard_size)] for i in range(self.chessboard_size)])
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        A = False
        print(len(idx))
        if (len(idx) == 224):
            pos_first = np.where(chessboard == -self.color)
            pos_first = list(zip(pos_first[0], pos_first[1]))
            pos_1 = pos_first[0]
            if ((pos_1[0] == 1 or pos_1[0] == 13) and (pos_1[1] == 1 or pos_1[1] == 13)):
                A = True
            else:
                A = False
        if (len(idx) == 225 or A):
            self.candidate_list.append([7, 7])

        else:
            COLOR = self.color
            print(COLOR)
            print(chessboard)
            self.candidate_list.clear()
            for pos in idx:
                value = self.calcute_value(chessboard, pos[0], pos[1], COLOR)
                if value > candidate_value[pos[0], pos[1]]:
                    candidate_value[pos[0], pos[1]] = value
            for pos in idx:
                value_temp = self.calcute_value(chessboard, pos[0], pos[1], -COLOR)
                if value_temp > 0:
                    value_temp = value_temp - 1
                    if value_temp > candidate_value[pos[0], pos[1]]:
                        candidate_value[pos[0], pos[1]] = value_temp
            pos_list = []
            temp_max = -1
            for pos in idx:
                if candidate_value[pos[0], pos[1]] > temp_max:
                    pos_list.clear()
                    pos_list.append(pos)
                    temp_max = candidate_value[pos[0], pos[1]]
                elif candidate_value[pos[0], pos[1]] == temp_max:
                    pos_list.append(pos)
            print(candidate_value)
            pos_index = random.randint(0, len(pos_list) - 1)
            new_pos = pos_list[pos_index]
            print(len(pos_list))
            assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
            self.candidate_list.append(new_pos)