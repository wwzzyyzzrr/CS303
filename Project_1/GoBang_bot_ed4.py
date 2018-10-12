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
        elif z[4] > 0:  # 活三
            value = 32
        elif z[5] > 0:  # 冲三
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

    def go_timeout(self, chessboard):
        COLOR = self.color
        print(chessboard)
        self.candidate_list.clear()
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        pos_idx = random.randint(0, len(idx) - 1)
        new_pos = idx[pos_idx]
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        print(new_pos)
        self.candidate_list.append(new_pos)

    def get_pos_list(self, chessboard, color):       
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
        pos_list = []
        temp_max = -10
        for pos in idx:
            if candidate_value[pos[0], pos[1]] > temp_max:
                pos_list.clear()
                pos_list.append(pos)
                temp_max = candidate_value[pos[0], pos[1]]
            elif candidate_value[pos[0], pos[1]] == temp_max:
                pos_list.append(pos)
        pos1 = pos_list[0]
        #print(candidate_value)
        return [pos_list, candidate_value[pos1[0], pos1[1]]]

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
            list_t_1 = self.get_pos_list(chessboard, self.color)
            pos_list_1 = list_t_1[0]
            if len(pos_list_1) == 1 or len(idx) <= 4:
                self.candidate_list.append(pos_list_1[0])
            else:
                chessboard_temp = copy.deepcopy(chessboard)
                pos_pull = pos_list_1[0]
                a1 = 0
                b1 = 0
                for pos in pos_list_1:
                    chessboard_temp[pos[0], pos[1]] = self.color
                    list_t_2 = self.get_pos_list(chessboard_temp, -self.color)
                    pos_list_2 = list_t_2[0]
                    chessboard_temp_2 = copy.deepcopy(chessboard_temp)
                    for pos1 in pos_list_2:
                        chessboard_temp_2[pos1[0],pos1[1]] = -self.color
                        list_t_3 = self.get_pos_list(chessboard_temp_2, self.color)
                        pos_list_3 = list_t_3[0]
                        chessboard_temp_3 = copy.deepcopy(chessboard_temp_2)
                        for pos2 in pos_list_3:
                            chessboard_temp_3[pos2[0], pos2[1]] = self.color
                            list_t_4 = self.get_pos_list(chessboard_temp_3, -self.color)
                            pos_list_4 = list_t_4[0]
                            chessboard_temp_4 = copy.deepcopy(chessboard_temp_3)
                            for pos3 in pos_list_4:
                                chessboard_temp_4[pos3[0], pos3[1]] = -self.color
                                pos_list_5 = self.get_pos_list(chessboard_temp_4, self.color)
                                if pos_list_5[1] < a1:
                                    break
                                elif pos_list_5[1] > a1:
                                    a1 = pos_list_5[1]
                                    b1 = len(pos_list_5[0])
                                    pos_pull = pos
                                elif pos_list_5[1] == a1 and len(pos_list_5[0]) > b1:
                                    b1 = len(pos_list_5[0])
                                    pos_pull = pos
                                chessboard_temp_4[pos3[0],pos3[1]] = COLOR_NONE
                            chessboard_temp_3[pos2[0],pos[1]] = COLOR_NONE
                        chessboard_temp_2[pos1[0], pos1[1]] = COLOR_NONE
                    chessboard_temp[pos[0], pos[1]] = COLOR_NONE
                self.candidate_list.append(pos_pull)
