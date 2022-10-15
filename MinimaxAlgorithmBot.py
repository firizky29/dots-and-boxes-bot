from GameAction import GameAction
from GameState import GameState

class MinimaxBot:
    def __init__(self, isPlayer1: bool):
        # var self.OPT: Group -> GameAction
        # var self.DELTA: Group -> Value of State yang didapt di masa depan.
        # isPlayer1
        self.OPT = [None for i in range(2**24)]
        self.DELTA = [-10 for i in range(2**24)]
        self.isPlayer1 = isPlayer1

    # fungsi get_result, terminal-test, utility, Max-state, Min-state, group. tambah fungsi value
    # current itu fungsi selish box player- lawan sekarang.
    # actions diganti jadi looping aja
    # def group(s: GameState) -> Int:
    #     # 1010000101

    
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