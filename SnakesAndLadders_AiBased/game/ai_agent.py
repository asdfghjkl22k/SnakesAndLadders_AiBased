from game.player import Player
import random

class AIPlayer(Player):
    def __init__(self, name="AI", color=(255, 0, 0)):
        super().__init__(name, color)

    def move(self, steps, board):
        # Currently behaves like a normal player; can be upgraded to smarter strategy
        print(f"{self.name} is thinking...")  # Placeholder for future AI delay or logic
        super().move(steps, board)

    # Example of a simple strategy you can expand later
    def choose_dice_roll(self):
        return random.randint(1, 6)  # Later: use probabilities or RL
