import Project_1.Gobang as Gobang
import Project_1.human as human
import Project_1.sb_bot as sb_bot

game = Gobang.Gobang()
p1 = sb_bot.AI(game.BOARD_SIZE, 1, 10000)
p2 = human.HumanPlayer(game.BOARD_SIZE, -1, 10000)
player = {1: p1, -1: p2}

# # test
# game.set_chessboard_state(5,5,1)
# game.set_chessboard_state(5,6,1)
# game.set_chessboard_state(5,7,1)
# player[1].go(game.get_chess_board())
# # end test

while True:
    print(game)
    lst_player = game.get_current_move()[2]
    cur_player = - lst_player
    print("Now player {0} go:".format(cur_player))
    try:
        player[cur_player].go(game.get_chess_board())
        nxt_move = player[cur_player].candidate_list[-1]
        winner = game.set_chessboard_state(nxt_move[0], nxt_move[1], cur_player)
    except Exception as e:
        print('\033[32;0m'+e.__str__()+'\033[0m')
        continue
    if winner != 0:
        print(('\033[1;32;40m'+"Player {0} win!"+'\033[1;32;40m').format(winner))
        break
