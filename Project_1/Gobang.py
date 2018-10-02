import numpy


class Gobang(object):
    BOARD_SIZE = 15
    WIN_STEP = 5
    DIR = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def __init__(self):
        self.__chess_board = numpy.array([[0 for j in range(self.BOARD_SIZE)] for i in range(self.BOARD_SIZE)])
        self.__current_move = (-1, -1, -1)
        self.__winner = 0
        self.__chess_board[4, 8] = 1
        self.__chess_board[7, 7] = 1
        self.__chess_board[5, 7] = -1
        self.__chess_board[6, 6] = -1

    def __str__(self):
        s = '  '
        for x in range(self.BOARD_SIZE):
            tmp = chr(ord('A')+x-10) if x >= 10 else str(x)
            s += tmp+' '
        s += '\n'
        s += '  '
        for x in range(self.BOARD_SIZE):
            s += '--'
        s += '\n'
        for x in range(self.BOARD_SIZE):
            tmp = chr(ord('A') + x - 10) if x >= 10 else str(x)
            s += tmp+'|'
            for y in range(self.BOARD_SIZE):
                if x == self.__current_move[0] and y == self.__current_move[1]:
                    s += '\033[4;31;0m'
                if self.__chess_board[x][y] == 0:
                    s += '. '
                elif self.__chess_board[x][y] == 1:
                    s += 'X '
                else:
                    s += 'O '
                if x == self.__current_move[ 0 ] and y == self.__current_move[ 1 ]:
                    s += '\033[0m'
            s += '\n'
        return s

    def get_chess_board(self):
        return self.__chess_board

    def get_current_move(self):
        return self.__current_move

    class InvalidMoveError(RuntimeError):
        def __init__(self, args):
            self.args = args

        def __str__(self):
            return self.args[0]

    def in_range(self, x, y):
        if x not in range(0, self.BOARD_SIZE) or y not in range(0, self.BOARD_SIZE):
            return False
        return True

    def check_win(self):
        same_color = [0 for i in range(8)]
        for i in range(8):
            cur = list(self.__current_move)
            for j in range(self.WIN_STEP-1):
                cur[0] += self.DIR[i][0]
                cur[1] += self.DIR[i][1]
                if not self.in_range(cur[0], cur[1]):
                    break
                if self.__chess_board[cur[0]][cur[1]] != cur[2]:
                    break
                same_color[i] += 1
        for i in range(4):
            if same_color[i]+same_color[i+4]+1 >= self.WIN_STEP:
                return True
        return False

    def set_chessboard_state(self, x, y, player):
        if self.__winner != 0:
            raise self.InvalidMoveError(("Player {0} has already win!".format(player),))
        if not self.in_range(x, y) or player not in (-1, 1):
            raise self.InvalidMoveError(("Invalid position or player!",))
        if self.__chess_board[x][y] != 0:
            raise self.InvalidMoveError(("Position had been occupied!",))
        self.__current_move = (x, y, player)
        self.__chess_board[x][y] = player
        if self.check_win():
            self.__winner = player
            return player
        return 0


