from os import stat
import numpy as np
from GameAction import GameAction
from GameState import GameState
from Bot import Bot
from time import sleep

class MinimaxBot(Bot):
    def __init__(self, isPlayer1: bool = False):
        # var self.OPT: Group -> GameAction
        # var self.DELTA: Group -> Value of State yang didapat di masa depan.
        # isPlayer1
        self.OPT = [None for i in range(2**24)]
        self.DELTA = [-10 for i in range(2**24)]
        self.isPlayer1 = isPlayer1

    # fungsi get_result, terminal-test, utility, Max-state, Min-state, group. tambah fungsi value
    # current itu fungsi selish box player- lawan sekarang.
    # actions diganti jadi looping aja
    def group(self, s: GameState) -> int:
        group_s = 0
        ct = 0
        for i in range(4):
            for j in range(3):
                if s.row_status[i][j] == 1:
                    group_s += 1<<ct 
                ct += 1
        for i in range(3):
            for j in range(4):
                if s.col_status[i][j] == 1:
                    group_s += 1<<ct
                ct +=1
        return group_s

    def terminal_test(self, state: GameState) -> bool:
        # cek apakah state sudah terminal atau belum
        """
        Returns true if state is terminal.
        State disebut terminal apabila setiap kotak sudah terisi 
        yang dalam hal ini status == 4 untuk setiap kolom dan baris.
        """
        [y, x] = state.board_status.shape

        for i in range(y):
            for j in range(x):
                if abs(state.board_status[i, j]) != 4:
                    return False
        return True

    
    def current_utility(self, state: GameState) -> int:
        """
        menghitung nilai utility sementara dari state saat ini untuk player 1, yaitu
        = selisih box player_1 - box player_2
        """
        [y, x] = state.board_status.shape
        skor_1 = 0
        skor_2 = 0
        for i in range(y):
            for j in range(x):
                if state.board_status[i, j] == 4:
                    skor_2 += 1
                elif state.board_status[i, j] == -4:
                    skor_1 += 1
        return skor_1 - skor_2

    def value(self, state: GameState) -> int:
        """
        Mengembalikan value/utilitas akhir yang didapat player 1 ketika kedua player bermain optimal.
        Prasyarat: DELTA[group(state)] sudah terisi
        """
        if(self.terminal_test(state)):
            self.DELTA[self.group(state)] = 0
            return self.current_utility(state)
        val = self.current_utility(state)
        if(state.player1_turn):
            val += self.DELTA[self.group(state)]
        else:
            val -= self.DELTA[self.group(state)]
        return val

    def Max_state(self, state: GameState, alpha: int, beta: int) -> GameAction:
        """
        Mengembalikan aksi yang optimal untuk player 1 yaitu memaksimalkan (box player 1 - box player 2).
        """
        # print(state)
        if(self.OPT[self.group(state)] is not None):
            return self.OPT[self.group(state)]
        if(self.terminal_test(state)):
            self.DELTA[self.group(state)] = 0
            return None
        state_value = -10
        act_OPT = None
        [yr, xr] = state.row_status.shape
        [yc, xc] = state.col_status.shape
        for i in range(yr):
            for j in range(xr):
                if (state.row_status[i][j]==0):
                    next_state = self.get_next_state(state, GameAction("row", (i,j)))
                    if(next_state.player1_turn):
                        self.Max_state(next_state, alpha, beta)
                    else:
                        self.Min_state(next_state, alpha, beta)
                    next_value = self.value(next_state)
                    if(next_value > state_value):
                        state_value = next_value
                        act_OPT = GameAction("row", (i,j))
                    if(state_value >= beta): 
                        # self.OPT[self.group(state)] = act_OPT
                        # self.DELTA[self.group(state)] = state_value - self.current_utility(state)
                        return act_OPT
                    alpha = max(alpha, state_value)
        
        for i in range(yc):
            for j in range(xc):
                if(state.col_status[i][j]==0):
                    next_state = self.get_next_state(state, GameAction("col", (i,j)))
                    if(next_state.player1_turn):
                        self.Max_state(next_state, alpha, beta)
                    else:
                        self.Min_state(next_state, alpha, beta)
                    next_value = self.value(next_state)
                    if(next_value > state_value):
                        state_value = next_value
                        act_OPT = GameAction("col", (i,j))
                    if(state_value >= beta):
                        if(i==yc-1 and j==xc-1):
                            self.OPT[self.group(state)] = act_OPT
                            self.DELTA[self.group(state)] = state_value - self.current_utility(state)
                        # self.OPT[self.group(state)] = act_OPT
                        # self.DELTA[self.group(state)] = state_value - self.current_utility(state)
                        return act_OPT
                    alpha = max(alpha, state_value)
        
        self.OPT[self.group(state)] = act_OPT
        self.DELTA[self.group(state)] = state_value - self.current_utility(state)
        print(state)
        print("Optimal: ", end="")
        print(self.OPT[self.group(state)])
        return act_OPT

    def get_next_state(self, state: GameState, action: GameAction) -> GameState:
        # return state baru
        """
        Returns new state based on current state and action.
        """
        action_type = action.action_type
        y, x = action.position

        new_state = GameState(state.board_status.copy(), state.row_status.copy(), state.col_status.copy(), state.player1_turn)
        [ny, nx] = new_state.board_status.shape
        player_in_turn = -1 if new_state.player1_turn else 1
        is_get_point = False

        if y < ny and x < nx:
            new_state.board_status[y, x] = (abs(new_state.board_status[y, x]) + 1) * player_in_turn
            if abs(new_state.board_status[y, x]) == 4:
                is_get_point = True
        
        if action_type == "row":
            new_state.row_status[y, x] = 1
            if y > 0:
                new_state.board_status[y-1, x] = (abs(new_state.board_status[y-1, x]) + 1) * player_in_turn
                if abs(new_state.board_status[y-1 , x]) == 4:
                    is_get_point = True
        elif action_type == "col":
            new_state.col_status[y, x] = 1
            if x > 0:
                new_state.board_status[y, x-1] = (abs(new_state.board_status[y, x-1]) + 1) * player_in_turn
                if abs(new_state.board_status[y, x-1]) == 4:
                    is_get_point = True
        
        decision = not (new_state.player1_turn ^ is_get_point)
        new_state = new_state._replace(player1_turn=decision)
        return new_state
    
    def Min_state(self, state: GameState, alpha: int, beta: int) -> GameAction:
        """
        Mengembalikan aksi yang optimal untuk player 2 yaitu meminimalkan (box player 1 - box player 2).
        """
        # print(state)
        # sleep(5)
        if(self.OPT[self.group(state)] is not None):
            return self.OPT[self.group(state)]
        if(self.terminal_test(state)):
            self.DELTA[self.group(state)] = 0
            return None
        state_value = 10
        act_OPT = None
        [yr, xr] = state.row_status.shape
        [yc, xc] = state.col_status.shape
        for i in range(yr):
            for j in range(xr):
                if (state.row_status[i][j]==0):
                    next_state = self.get_next_state(state, GameAction("row", (i,j)))
                    if(next_state.player1_turn):
                        self.Max_state(next_state, alpha, beta)
                    else:
                        self.Min_state(next_state, alpha, beta)
                    next_value = self.value(next_state)
                    if(next_value < state_value):
                        state_value = next_value
                        act_OPT = GameAction("row", (i,j))
                    if(state_value <= alpha): 
                        # self.OPT[self.group(state)] = act_OPT
                        # self.DELTA[self.group(state)] = state_value - self.current_utility(state)
                        return act_OPT
                    beta = min(beta, state_value)
        
        for i in range(yc):
            for j in range(xc):
                if(state.col_status[i][j]==0):
                    next_state = self.get_next_state(state, GameAction("col", (i,j)))
                    if(next_state.player1_turn):
                        self.Max_state(next_state, alpha, beta)
                    else:
                        self.Min_state(next_state, alpha, beta)
                    next_value = self.value(next_state)
                    if(next_value < state_value):
                        state_value = next_value
                        act_OPT = GameAction("col", (i,j))
                    if(state_value <= alpha):
                        if(i==yc-1 and j==xc-1):
                            self.OPT[self.group(state)] = act_OPT
                            self.DELTA[self.group(state)] = (state_value - self.current_utility(state))*(-1)
                        # self.OPT[self.group(state)] = act_OPT
                        # self.DELTA[self.group(state)] = state_value - self.current_utility(state)
                        return act_OPT
                    beta = min(beta, state_value)

        self.OPT[self.group(state)] = act_OPT
        self.DELTA[self.group(state)] = (state_value - self.current_utility(state))*(-1)
        print(state)
        print("Optimal: ", end="")
        print(self.OPT[self.group(state)])        
        return act_OPT

    
    """
    An interface for bot. Inherit it to create your own bots!
    """
    def get_action(self, state: GameState) -> GameAction:
        # panggil Max, Min sesuai nomor player
        """
        Returns action based on state.
        """
        act_i = None
        if(self.isPlayer1):
            act_i = self.Max_state(state,-10,10)
        else:
            act_i = self.Min_state(state,-10,10)
        return GameAction(act_i.action_type, (act_i.position[1], act_i.position[0]))

# mnmx = MinimaxBot(False)
# if(mnmx.OPT[3] is None):
#     print("mnmx.OPT[3] is None")
# mnmx.OPT[3] = GameAction("row", (3,2))
# if(mnmx.OPT[3] is None):
#     print("mnmx.OPT[3] is None")
# gs = GameState([[1,-2,4],[1,2,2],[2,4,2]], [[0,0,1],[0,0,1],[0,1,0],[0,1,0]], [[0,1,1,1],[0,1,0,1],[1,1,1,1]], True)

def test_group():
    gs = GameState([[1,-2,4],[1,2,2],[2,4,2]], [[0,0,1],[0,0,1],[0,1,0],[0,1,0]], [[0,1,1,1],[0,1,0,1],[1,1,1,1]], True)
    print(bin(mnmx.group(gs)))

# test_group()

def test_current():
    board_status = np.array([[1,-2,4],[1,2,2],[2,4,2]])
    gs = GameState(board_status, [[0,0,1],[0,0,1],[0,1,0],[0,1,0]], [[0,1,1,1],[0,1,0,1],[1,1,1,1]], True)
    print(mnmx.current_utility(gs))

def test_step3():
    mnmx = MinimaxBot(True)
    board_status = np.array([[2,0,0],[1,0,0],[0,0,0]])
    row_status = np.array([[1,0,0],[1,0,0],[0,0,0],[0,0,0]])
    col_status = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    gs = GameState(board_status, row_status, col_status, True)
    ans = mnmx.get_action(gs)
    print("ans is ", end="")
    print(ans)

def test_step1():
    mnmx = MinimaxBot(True)
    board_status = np.array([[0,0,0],[0,0,0],[0,0,0]])
    row_status = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0]])
    col_status = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    gs = GameState(board_status, row_status, col_status, True)
    ans = mnmx.get_action(gs)
    print("ans is ", end="")
    print(ans)        

# test_current()
mnmx = MinimaxBot(True)
board_status = np.array([[0,0,0],[0,0,0],[0,0,0]])
row_status = np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0]])
col_status = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0]])
gs = GameState(board_status, row_status, col_status, True)
ans = mnmx.get_action(gs)
print("ans is ", end="")
print(ans)
print("DELTA ",end="")
print(mnmx.DELTA[10838015])    
print("current util", end="")
print(mnmx.current_utility(gs))  

# import sys
# print(sys.getrecursionlimit())
# gs = mnmx.get_next_state(gs,ans)
# ans = GameAction("col",(0,0))
# gs = mnmx.get_next_state(gs,ans)
# ans = mnmx.get_action(gs)
# print("ans is ", end="")
# print(ans)
# gs = mnmx.get_next_state(gs,ans)
# ans = GameAction("col",(1,0))
# gs = mnmx.get_next_state(gs,ans)
# ans = mnmx.get_action(gs)
# print("ans is ", end="")
# print(ans)
# gs = mnmx.get_next_state(gs,ans)
# ans = GameAction("col",(2,0))
# gs = mnmx.get_next_state(gs,ans)
# ans = mnmx.get_action(gs)
# print("ans is ", end="")
# print(ans)
# gs = mnmx.get_next_state(gs,ans)
# ans = GameAction("col",(0,1))
# gs = mnmx.get_next_state(gs,ans)
# ans = GameAction("col",(0,3))
# gs = mnmx.get_next_state(gs,ans)
# ans = mnmx.get_action(gs)
# print("ans is ", end="")
# print(ans)
# gs = mnmx.get_next_state(gs,ans)
# ans = GameAction("col",(0,2))
# gs = mnmx.get_next_state(gs,ans)
# ans = GameAction("row",(1,2))
# gs = mnmx.get_next_state(gs,ans)
# ans = GameAction("col",(2,1))
# gs = mnmx.get_next_state(gs,ans)
# ans = mnmx.get_action(gs)
# print("ans is ", end="")
# print(ans)
# gs = mnmx.get_next_state(gs,ans)
