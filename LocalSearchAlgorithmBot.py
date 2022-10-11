from GameAction import GameAction
from GameState import GameState
from Bot import Bot

class state:

    def __init__(self, ):
        self.value = 0
    
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
        return math.exp(deltaE, temperature)
    
    def schedule(self, t):
        temp = 100 - 2*t
        if temp>0:
            return temp
        else:
            return 0
    