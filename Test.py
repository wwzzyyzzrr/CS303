import copy

list1 = [1,2,3,4,5]
list2 = copy.deepcopy(list1)
list1.clear()
print(list2)

a = 1
b = -a
print(b)

'''
        elif(len(idx) == 223 and chessboard[7,7] == COLOR_NONE):
            self.candidate_list.append([7, 7])
        elif(len(idx) == 221 and chessboard[6,7] == COLOR_NONE):
            self.candidate_list.append([6,7])
        '''

'''
            if (len(idx) == 219 and chessboard[8, 7] == COLOR_NONE and chessboard[6, 7] == self.color):
                if (self.calcute_value(chessboard,pos[0],pos[1],-self.color) < 40 and self.calcute_value(chessboard,pos[0],pos[1],self.color)<40):
                    self.candidate_list.append([8, 7])
            '''