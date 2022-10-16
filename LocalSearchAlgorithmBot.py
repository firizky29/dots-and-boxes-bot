from GameAction import GameAction
from GameState import GameState
from Bot import Bot
import math


    
class LocalSearchBot(Bot):
    
    def __init__(self, isPlayer1: bool, temperature: int):
        self.isPlayer1 = isPlayer1
        self.T = temperature
        


    def get_action(self, state: GameState) -> GameAction:
        """
        Returns action based on state.
        """
        raise NotImplementedError()

    def get_random_state(self, state: GameState) -> GameState:
        """
        Returns a random state
        """
        raise NotImplementedError()
    
    def get_state_value(self, state: GameState) -> int:
        """
        Returns a value of state
        """
        raise NotImplementedError()

    
    def probability(self, deltaE, temperature):
        return math.exp(deltaE, temperature)
    
    def schedule(self, t):
        temp = self.T - 2*t
        if temp>0:
            return temp
        else:
            return 0
    