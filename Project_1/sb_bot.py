import numpy as np
import random

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

class AI(object):

    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self, chessboard):
        COLOR = COLOR_BLACK
        print(chessboard)
        self.candidate_list.clear()
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        pos_idx = random.randint(0, len(idx) - 1)
        new_pos = idx[pos_idx]
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        print(new_pos)
        self.candidate_list.append(new_pos)

