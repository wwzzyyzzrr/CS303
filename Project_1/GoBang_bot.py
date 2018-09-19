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

    def go(self, chessboard):
        self.candidate_list.clear()
