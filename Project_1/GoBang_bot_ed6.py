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
            elif -1 < a + 2 * j < 15 and -1 < b + 2 * k < 15:
                if chessboard[a + 2 * j, b + 2 * k] == COLOR:
                    m = i
                    flag = 1
                else:
                    a = a + j
                    b = b + k
                    break
            a = a + j
            b = b + k
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
            if enough == 0:
                if (x[i][1] >= 1 and x[i+4][0]>=3) or (x[i][0]>=1 and x[i+4][1]>=3) or (x[i][1] >= 1 and x[i+4][0]>=3) or (x[i][0]>=3 and x[i+4][1]>=1):
                    y.append(11)#长连5
                elif (x[i][1] >= 1 and x[i+4][0]>=2) or (x[i][0] >= 2 and x[i+4][1]>=1) or (x[i][1] >= 2 and x[i+4][0]>=1) or (x[i][0] >= 1 and x[i+4][1]>=2):
                    y.append(12)#长连4
                elif (x[i][1] >= 1 and x[i+4][1]>=1):
                    y.append(13)#双长连
                elif (-4< x[i][1] * x[i+4][1] <0 or (x[i][1]==-1 and x[i+4][1]==-1)):
                    y.append(10)


        z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for m in y:
            z[m] = z[m] + 1
        if z[1] > 0:
            value = 100
        elif (z[2] > 0 and (z[3] > 0 or z[4] > 0)):
            value = 60 + z[3] * 6 + z[4] * 4
        elif z[2] > 0:
            value = 60
        elif z[3] > 1:  # 双冲四
            value = 56
        elif (z[3] > 0 and z[4] > 0):  # 四三
            value = 52
        elif z[4] > 1:  # 双三
            value = 48
        elif (z[4] > 0 and z[5] > 0):  # 活三+冲三
            value = 44
        elif z[3] > 0:  # 冲四
            value = 40
        elif (z[4] > 0 and z[6] > 0):  # 活三 + 活二
            value = 36
        elif z[11] > 0:
            value = 34
        elif z[4] > 0 :  # 活三
            value = 32
        elif z[5] > 0 or z[12] > 0:  # 冲三
            value = 28 + z[5] + z[12]
        elif (z[5] > 0 and a[6] > 0) or z[13]>0:  # 冲三+活二
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

    def get_pos_value(self, chessboard, color):
        candidate_value = np.array([[-2 for j in range(self.chessboard_size)] for i in range(self.chessboard_size)])
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        self.candidate_list.clear()
        COLOR = color
        for pos in idx:
            value = self.calcute_value(chessboard, pos[0], pos[1], COLOR)
            if value > candidate_value[pos[0], pos[1]]:
                candidate_value[pos[0], pos[1]] = value
        COLOR = -color
        for pos in idx:
            value = self.calcute_value(chessboard, pos[0], pos[1], COLOR)
            if value > 0:
                value = value - 1
                if value > candidate_value[pos[0], pos[1]]:
                    candidate_value[pos[0], pos[1]] = value
        return candidate_value

    def get_pos_list(self,chessboard,COLOR):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        candidate_value = self.get_pos_value(chessboard, COLOR)
        max_list = []
        max_second_list = []
        temp_max = -10
        temp_max_second = -10
        for pos in idx:
            value_temp = candidate_value[pos[0], pos[1]]
            if value_temp > temp_max:
                max_second_list = copy.deepcopy(max_list)
                max_list.clear()
                max_list.append(pos)
                temp_max_second = temp_max
                temp_max = value_temp
            elif value_temp == temp_max:
                max_list.append(pos)
            else:
                if value_temp > temp_max_second:
                    max_second_list.clear()
                    max_second_list.append(pos)
                elif value_temp == temp_max_second:
                    max_second_list.append(pos)
        pos_list = max_list
        return pos_list

    def tree(self, chessboard, alpha_beta,value ,pos_list,time):
        for pos in pos_list:
            if time < 4:
                chessboard[pos[0],pos[1]] = alpha_beta
                idx = np.where(chessboard == COLOR_NONE)
                idx = list(zip(idx[0], idx[1]))
                pos_list_temp = idx
                value_temp = self.tree(chessboard,-alpha_beta,value,pos_list_temp,time+1)
                chessboard[pos[0], pos[1]] = 0
                if alpha_beta == -self.color:
                    if value_temp[1] > value[0]:
                        value[0] = copy.deepcopy(value_temp[1])
                    else:
                        break
                else:
                    if value_temp[0] < value[1]:
                        value[1] = copy.deepcopy(value_temp[0])
                    else:
                        break
            else:
                chessboard[pos[0], pos[1]] = alpha_beta
                if alpha_beta == self.color:
                    value_temp = [self.calcute_value(chessboard, pos[0], pos[1], alpha_beta),10000]
                else:
                    value_temp = [-10000,self.calcute_value(chessboard, pos[0], pos[1], alpha_beta)]
                self.interger = self.interger + 1
                chessboard[pos[0], pos[1]] = 0
                if alpha_beta == -self.color:
                    if value_temp[1] > value[0]:
                        value[0] = copy.deepcopy(value_temp[1])
                    else:
                        break
                else:
                    if value_temp[0] < value[1]:
                        value[1] = copy.deepcopy(value_temp[0])
                    else:
                        break
        return value

    def go(self, chessboard):
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
            chessboard_temp = copy.deepcopy(chessboard)
            pos_list = self.get_pos_list(chessboard,self.color)
            alpha_value = -10000
            #pos = pos_list[0]
            pos_set = []
            print(pos_list)
            cal_value = self.calcute_value(chessboard, pos_list[0][0], pos_list[0][1], self.color)
            cal_value_temp = self.calcute_value(chessboard, pos_list[0][0], pos_list[0][1], -self.color) - 1
            if cal_value < cal_value_temp:
                cal_value = cal_value_temp
            if cal_value > 48:
                self.candidate_list.append(pos_list[0])
            else:
                self.interger = 0
                for pos in pos_list:
                    chessboard_temp[pos[0],pos[1]] = self.color
                    pos_list_temp = self.get_pos_list(chessboard_temp,-self.color)
                    value = self.tree(chessboard_temp, self.color,[-10000,10000],pos_list_temp,0)
                    chessboard_temp[pos[0],pos[1]] = COLOR_NONE
                    if value[0] > alpha_value:
                        alpha_value = copy.deepcopy(value[0])
                        pos_set.clear()
                        pos_set.append(pos)
                    elif value[0] == alpha_value:
                        pos_set.append(pos)
                pos = pos_set[random.randint(0,len(pos_set)-1)]
                print(pos_set)
                print(self.interger)
                self.candidate_list.append(pos)