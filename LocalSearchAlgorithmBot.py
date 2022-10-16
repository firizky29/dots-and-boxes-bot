from random import randrange
from GameAction import GameAction
from GameState import GameState
from Bot import Bot
import math
import random
import numpy as np

BOX_ROW = 3
MAX_ROW_I = BOX_ROW
MAX_ROW_J = BOX_ROW-1
MAX_COL_I = BOX_ROW-1
MAX_COL_J = BOX_ROW

class State:
    
    def __init__(self, game_status: GameState):
        self.board = game_status.board_status.copy()
        self.row = game_status.row_status.copy()
        self.col = game_status.col_status.copy()
        self.is_player1 = game_status.player1_turn
        
        self.value = BOX_ROW*BOX_ROW
        for i in range(BOX_ROW):
            for j in range(BOX_ROW):
                if(abs(self.board[i][j]) == 4):
                    self.value += self.board[i][j]/4
    
    # ketika state diberi aksi
    # gajelas bgt ini dah T_T
    def set_action(self, act, i, j):
        if(act == 'row'):
            self.row[i][j] = 1
            if(i<MAX_ROW_I):
                self.board[i][j] = abs(self.board[i][j])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
            if(i>0):
                self.board[i][j] = abs(self.board[i-1][j])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
            if(j<MAX_ROW_J):
                self.board[i][j] = abs(self.board[i][j])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
            if(j>0):
                self.board[i][j] = abs(self.board[i][j-1])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
        else:
            self.col[i][j] = 1
            if(i<MAX_COL_I):
                self.board[i][j] = abs(self.board[i][j])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
            if(i>0):
                self.board[i][j] = abs(self.board[i-1][j])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
            if(j<MAX_COL_J):
                self.board[i][j] = abs(self.board[i][j])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
            if(j>0):
                self.board[i][j] = abs(self.board[i][j-1])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
            
    def update_val(self):
        for i in range(BOX_ROW):
            for j in range(BOX_ROW):
                if(self.board[i][j] == 4):
                    self.value += self.board[i][j]/4
    
class LocalSearchBot(Bot):
    """
    An interface for bot. Inherit it to create your own bots!
    """
    def get_action(self, state: GameState) -> GameAction:
        """
        Returns action based on state.
        """
        raise NotImplementedError()
    
    def probability(self, deltaE, temperature):
        return math.exp(deltaE/temperature)
    
    def schedule(self, t):
        temp = 100 - 2*t
        if temp>0:
            return temp
        else:
            return 0
    
    def randomize(self, x, y):
        i = random.randint(0,x-1)
        j = random.randint(0,y-1)
        return (i,j)

    def get_successor(self, current: State):
        all_row_marked = np.all(current.row == 1)
        all_col_marked = np.all(current.col == 1)
        successor = State(current)
        act = random.choice(['row', 'col'])
        if(act == 'row' and not all_row_marked):
            (i,j) = self.randomize(BOX_ROW+1,BOX_ROW)
            while(successor.row[i][j] == 1):
                successor = State(current)
            
                
        else:
            i = random.randint(0,2)
            j = random.randint(0,3)   
             
    def SA(self, state: GameState):
        current = State(state)
        deltaE = 
        
    