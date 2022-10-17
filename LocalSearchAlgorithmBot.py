from operator import delitem
from random import randrange
import threading
from GameAction import GameAction
from GameState import GameState
from Bot import Bot
import math
import random
import numpy as np



class State:
    
    def __init__(self, game_status: GameState):
        self.board = game_status.board_status.copy()
        self.row = game_status.row_status.copy()
        self.col = game_status.col_status.copy()
        self.is_player1 = game_status.player1_turn
        [self.nboardx, self.nboardy] = self.board.shape
        [self.nrowx, self.nrowy] = self.row.shape
        [self.ncolx, self.ncoly] = self.col.shape
        self.value = 0

        # define heuristic value
        # prevent value from being negative
        self.value = self.nboardx*self.nboardy*3 
        for i in range(self.nboardx):
            for j in range(self.nboardy):
                if(abs(self.board[i][j]) == 3):
                    self.value += -3
                else:
                    self.value += abs(self.board[i][j])
    
    # ketika state diberi aksi
    # gajelas bgt ini dah T_T
    def set_action(self, action: GameAction):
        (act, (i, j)) = (action.action_type, action.position)
        if(act == 'row'):
            self.row[i][j] = 1
            if(i>0):
                self.board[i-1][j] = abs(self.board[i-1][j])+1
                if not self.is_player1:
                    self.board[i-1][j] *= -1
            if(i<self.nrowx-1):
                self.board[i][j] = abs(self.board[i][j])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
        else:
            self.col[i][j] = 1
            if(j<self.ncoly-1):
                self.board[i][j] = abs(self.board[i][j])+1
                if not self.is_player1:
                    self.board[i][j] *= -1
            if(j>0):
                self.board[i][j-1] = abs(self.board[i][j-1])+1
                if not self.is_player1:
                    self.board[i][j-1] *= -1


    def rollback_action(self, action: GameAction):
        (act, (i, j)) = (action.action_type, action.position)
        if(act == 'row'):
            self.row[i][j] = 0
            if(i>0):
                self.board[i-1][j] = abs(self.board[i-1][j])-1
                if not self.is_player1:
                    self.board[i-1][j] *= -1
            if(i<self.nrowx-1):
                self.board[i][j] = abs(self.board[i][j])-1
                if not self.is_player1:
                    self.board[i][j] *= -1
        else:
            self.col[i][j] = 0
            if(j<self.ncoly-1):
                self.board[i][j] = abs(self.board[i][j])-1
                if not self.is_player1:
                    self.board[i][j] *= -1
            if(j>0):
                self.board[i][j-1] = abs(self.board[i][j-1])-1
                if not self.is_player1:
                    self.board[i][j-1] *= -1

            
    def update_val(self):
        for i in range(self.nboardx):
            for j in range(self.nboardy):
                if(abs(self.board[i][j]) == 3):
                    self.value += -3
                else:
                    self.value += abs(self.board[i][j])

    
class LocalSearchBot(Bot):
    
    def __init__(self, isPlayer1: bool, temperature: int = 36):
        self.isPlayer1 = isPlayer1
        self.T = temperature


    def get_action(self, state: GameState) -> GameAction:
        # generate all possible actions
        # restart temperature
        self.T = 36
        current = GameState(state.board_status.copy(), state.row_status.copy(), state.col_status.copy(), state.player1_turn)
        (act, final_state) = self.simulated_annealing(current)
        return GameAction(act.action_type, (act.position[1], act.position[0]))

    
    def probability(self, deltaE, temperature):
        return math.exp(deltaE/temperature)
    
    def schedule(self, t):
        temp = self.T - 2*t
        if temp>0:
            return temp
        else:
            return 0

    def get_initial_state(self, current: GameState):
        initial = State(current)
        act = random.choice(self.get_all_possible_action(initial))
        initial.set_action(act)
        initial.update_val()

        return (act, initial)

    def get_successor(self, current: State, last_action: GameAction):
        successor = current
        possible_actions = self.get_all_possible_action(successor, last_action)
        if(len(possible_actions)):
            act = random.choice(possible_actions)
            successor.rollback_action(last_action)
            successor.set_action(act)
            successor.update_val()
            return (act, successor)
        else:
            return (last_action, successor)



    def get_all_possible_action(self, current: State, last_action = None) -> list:
        all_row_marked = np.all(current.row == 1)
        all_col_marked = np.all(current.col == 1)

        [nrowx, nrowy] = current.row.shape
        [ncolx, ncoly] = current.col.shape

        possible_action = []
        if not all_row_marked:
            for i in range(nrowx):
                for j in range(nrowy):
                    if current.row[i][j] == 0:
                        if(last_action is not None):
                            (act, (x, y)) = (last_action.action_type, last_action.position)
                            # prevent same action
                            if(act == 'row' and x == i and y == j):
                                continue
                        possible_action.append(GameAction('row', (i,j)))
        if not all_col_marked:
            for i in range(ncolx):
                for j in range(ncoly):
                    if current.col[i][j] == 0:
                        if(last_action is not None):
                            (act, (x, y)) = (last_action.action_type, last_action.position)
                            # prevent same action
                            if(act == 'col' and x == i and y == j):
                                continue
                        possible_action.append(GameAction('col', (i,j)))
        return possible_action
  
             
    def simulated_annealing(self, initial: GameState):

        # randomize initial state
        (best_action, current) = self.get_initial_state(initial)

        t = 1
        while True:
            self.T = self.schedule(t)
            if(self.T == 0):
                return (best_action, current)
            (best_action, successor) = self.get_successor(current, best_action)
            deltaE = successor.value - current.value
            if deltaE > 0:
                current = successor
            else:
                if random.uniform(1, math.exp(1)) >= self.probability(deltaE, self.T):
                    current = successor
            t += 1
        
    