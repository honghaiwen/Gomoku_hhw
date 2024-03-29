from chessboard import ChessBoard
from AI import MinMax,MinMax_smallset,MinMax_best
from MCTS import MCTS,MCTS_better
#from ai import searcher
import time

from const_set import *
import random
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound

class ChoiceOfPlayer(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(int, int)

    # 构造函数里增加形参
    def __init__(self,board,player_type,my_is_black,parent=None):
        super(ChoiceOfPlayer,self).__init__()
        self.type = player_type
        self.board = board
        self.my_is_black = my_is_black
        self.is_black = True
        self.parent = parent

        if(self.type == 0):
            self.Player = HumanPlayer(board,my_is_black)
        elif(self.type == 1):
            self.Player = AIPlayer_1(board,my_is_black)
        elif(self.type == 2):
            self.Player = AIPlayer_2(board,my_is_black)
        elif(self.type == 3):
            self.Player = AIPlayer_3(board,my_is_black)
        elif(self.type == 4):
            self.Player = AIPlayer_4(board,my_is_black)

    def run(self):
        while(1):
            time.sleep(0.5)

                

            if self.my_is_black == self.is_black:
                if self.my_is_black == True:
                    self.parent.mouse_point.setPixmap(self.parent.black)
                else:
                    self.parent.mouse_point.setPixmap(self.parent.white)
                not_empty = True
                while(not_empty):
                    #print("my_is_black:" + str(self.my_is_black))
                    i,j = self.Player.Go(self.parent.chessboard,self.is_black,self.parent)
                    
                    if not i is None and not j is None:
                        if self.parent.chessboard.get_xy_on_logic_state(i,j) == EMPTY:
                            not_empty = False

                

                self.finishSignal.emit(i, j)
                self.is_black = not self.is_black
                if self.my_is_black == True:
                    self.parent.player_white.is_black = False
                else:
                    self.parent.player_black.is_black = True

class HumanPlayer():
    def __init__(self, board,is_black):
        print('human')


    def Go(self,board,is_black,parent):
        self.board = board
        self.Going = True
        parent.Going = True
        while(parent.Going):
            time.sleep(0.1)

        i, j = self.coordinate_transform_pixel2map(parent.x,parent.y)
        return i,j

    def coordinate_transform_pixel2map(self, x, y):
        # 从 UI 上的绘制坐标到 chessMap 里的逻辑坐标的转换
        i, j = int(round((y - MARGIN) / GRID)), int(round((x - MARGIN) / GRID))
        # 有MAGIN, 排除边缘位置导致 i,j 越界
        if i < 0 or i >= N_LINE or j < 0 or j >= N_LINE:
            return None, None
        else:
            return i, j


    	


class AIPlayer_1():
    def __init__(self,board,is_black):
        self.ai = MinMax(is_black,1)
        print('AI_1')


    def Go(self,board,is_black,parent):
        result = self.ai.get_move(board)
        return result



class AIPlayer_2():
    def __init__(self,board,is_black):
        self.ai = MinMax_best(is_black)
        print('AI_2')


    def Go(self,board,is_black,parent):
        result = self.ai.get_move(board)
        return result

class AIPlayer_3():
    def __init__(self,board,is_black):
        self.ai = MinMax_smallset(is_black)
        print('AI_3')


    def Go(self,board,is_black,parent):
        result = self.ai.get_move(board)
        return result

class AIPlayer_4(): # MCTS
    def __init__(self,board,is_black):
        self.ai = MCTS_better(is_black)
        print('AI_4')


    def Go(self,board,is_black,parent):

        if is_black == True:
            color = BLACK
        else:
            color = WHITE

        result = self.ai.get_move(board,color)
        return result


# class RandomPlayer():
#     def __init__(self, board,is_black):
#         print('RandomPlayer')


#     def Go(self,board,is_black,parent):
#         board = parent.chessboard.board()
#         legal,a,b = parent.chessboard.get_board_item()
#         total = len(legal)
#         t = random.randint(0,total-1)
#         return legal[t]