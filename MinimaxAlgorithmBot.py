from GameAction import GameAction
from GameState import GameState

class MinimaxBot:
    # def __init__(self):
        # var self.OPT: Group -> GameAction
        # var self.DELTA: Group -> Value of State yang didapt di masa depan.
        # isPlayer1
        # value: dictionary of state and value

    # fungsi get_result, terminal-test, utility
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
