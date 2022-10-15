from os import stat
from GameAction import GameAction
from GameState import GameState
from Bot import Bot

class MinimaxBot(Bot):
    def __init__(self, isPlayer1: bool):
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
        menghitung nilai utility sementara dari state saat ini, yaitu
        = selisih box player - box lawan
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
        if(self.isPlayer1):
            return skor_1 - skor_2
        else:
            return skor_2 - skor_1

    def value(self, state: GameState) -> int:
        """
        Mengembalikan value/utilitas akhir yang didapat bot ketika kedua player bermain optimal.
        Prasyarat: DELTA[group(state)] sudah terisi
        """
        if(self.terminal_test(state)):
            self.DELTA[self.group(state)] = 0
            return self.current_utility(state)
        val = self.current_utility(state)
        if(state.isPlayer1 == self.isPlayer1):
            val += self.DELTA[self.group(state)]
        else:
            val -= self.DELTA[self.group(state)]
        return val

    
    """
    An interface for bot. Inherit it to create your own bots!
    """
    def get_action(self, state: GameState) -> GameAction:
        # panggil Max, Min sesuai nomor player
        """
        Returns action based on state.
        """
        raise NotImplementedError()

mnmx = MinimaxBot(True)
if(mnmx.OPT[3] is None):
    print("mnmx.OPT[3] is None")
mnmx.OPT[3] = GameAction("row", (3,2))
if(mnmx.OPT[3] is None):
    print("mnmx.OPT[3] is None")
gs = GameState([[1,-2,4],[1,2,2],[2,4,2]], [[0,0,1],[0,0,1],[0,1,0],[0,1,0]], [[0,1,1,1],[0,1,0,1],[1,1,1,1]], True)

def test_group():
    gs = GameState([[1,-2,4],[1,2,2],[2,4,2]], [[0,0,1],[0,0,1],[0,1,0],[0,1,0]], [[0,1,1,1],[0,1,0,1],[1,1,1,1]], True)
    print(bin(mnmx.group(gs)))

test_group()