import Gobang


class HumanPlayer(object):
    def __init__(self, chessboard_size, color, time_out):
        self.color = color
        self.candidate_list = []

    def go(self, chessboard):
        self.candidate_list.clear()
        try:
            x, y = map(int, (input().split()))
        except Exception as e:
            print("Error input")
            return -1, -1, self.color
        self.candidate_list.append((x, y))
