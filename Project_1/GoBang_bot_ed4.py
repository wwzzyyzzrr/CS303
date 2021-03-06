# -*- coding:utf-8 -*
import numpy as np
import random
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
        while (-1 < a + j < 15 and -1 < b + k < 15 and chessboard[a + j, b + k] == COLOR):
            i = i + 1
            a = a + j
            b = b + k
        if (-1 < a + j < 15 and -1 < b + k < 15):
            if chessboard[a + j, b + k] == COLOR_NONE:
                i = i * 2
            else:
                i = i * 2 - 1
        else:
            i = i * 2 - 1
        return i

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
            flag = x[i] + x[i + 4]
            if flag > 6:
                y.append(1)
            elif flag == 6:
                if (x[i] * x[i + 4] < 0 or x[i] == x[i + 4] or (x[i] == 5 or x[i + 4] == 5)):
                    y.append(1)  # 五连
                else:
                    y.append(2)  # 活四
            elif flag == 5:
                y.append(3)  # 冲四
            elif flag == 4:
                if (x[i] * x[i + 4] < 0):
                    y.append(10)  # 死四
                else:
                    y.append(4)  # 活三
            elif flag == 3:
                y.append(5)  # 冲三
            elif flag == 2:
                if (x[i] == x[i + 4] or x[i] * x[i + 4] < 0):
                    y.append(10)  # 死二死三
                else:
                    y.append(6)  # 活二
            elif flag == 1:
                y.append(7)  # 冲二
            elif flag == 0:
                if (x[i] * x[i + 4]) == 0:
                    y.append(8)  # 活一
                else:
                    y.append(10)  # 死二
            elif flag == -1:
                y.append(9)  # 冲一

        z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for m in y:
            z[m] = z[m] + 1
        if z[1] > 0:
            value = 1000000
        elif (z[2] > 0 and (z[3] > 0 or z[4] > 0)):
            value = 50000 + z[3] * 6000 + z[4] * 4000
        elif z[2] > 0:
            value = 50000
        elif z[3] > 1:  # 双冲四
            value = 45000
        elif (z[3] > 0 and z[4] > 0):  # 四三
            value = 45000
        elif z[4] > 1:  # 双三
            value = 20000
        elif (z[4] > 0 and z[5] > 0):  # 活三+冲三
            value = 1000
        elif z[3] > 0:  # 冲四
            value = 500
        elif (z[4] > 0 and z[6] > 0):  # 活三 + 活二
            value = 250
        elif z[4] > 0:  # 活三
            value = 125
        elif z[5] > 0:  # 冲三
            value = 64 + z[5] * 2
        elif (z[5] > 0 and a[6] > 0):  # 冲三+活二
            value = 32
        elif z[6] > 0:  # 活二
            value = 16 + z[6] * 2
        elif z[7] > 0:  # 冲二
            value = 8
        elif z[8] > 0:  # 活一
            value = 4
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
            value = self.calcute_value(chessboard, pos[0], pos[1], COLOR) + 0.9*self.calcute_value(chessboard, pos[0], pos[1], -COLOR)
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
        if temp_max-temp_max_second < 5 and temp_max<0:
            pos_list = max_list + max_second_list
        else:
            pos_list = max_list
        if len(pos_list) > 20:
            pos_list = pos_list[0:7]
        return pos_list

    def tree(self, chessboard, alpha_beta,value ,pos_list,time):
        for pos in pos_list:
            if time < 2:
                chessboard[pos[0],pos[1]] = alpha_beta
                pos_list_temp = self.get_pos_list(chessboard, -alpha_beta)
                value_temp = self.tree(chessboard,-alpha_beta,value,pos_list_temp,time+1)
                chessboard[pos[0], pos[1]] = 0
                if alpha_beta == self.color:
                    if value_temp[1] > value[0]:
                        value[0] = copy.deepcopy(value_temp[1])
                else:
                    if value_temp[0] < value[1]:
                        value[1] = copy.deepcopy(value_temp[0])
                if value[0] > value[1]:
                    break
            else:
                chessboard[pos[0], pos[1]] = alpha_beta

                value_temp = self.calcute_value(chessboard, pos[0], pos[1], alpha_beta)

                self.interger = self.interger + 1
                chessboard[pos[0], pos[1]] = 0
                value[0] = value_temp
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
            alpha_value = -1000000
            #pos = pos_list[0]
            pos_set = []
            print(pos_list)
            cal_value = self.calcute_value(chessboard, pos_list[0][0], pos_list[0][1], self.color)+self.calcute_value(chessboard, pos_list[0][0], pos_list[0][1], -self.color)
            if cal_value > 20000:
                self.candidate_list.append(pos_list[0])
            else:
                self.interger = 0
                for pos in pos_list:
                    chessboard_temp[pos[0],pos[1]] = self.color
                    pos_list_temp = self.get_pos_list(chessboard_temp,-self.color)
                    value = self.tree(chessboard_temp, self.color,[-1000000,1000000],pos_list_temp,0)
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