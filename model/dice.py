from utils.random_generator import RandomGenerator

class Dice:
    def __init__(self):
        self.random = RandomGenerator()

    def roll(self):
        """Roll two dice and return their sum."""
        die1 = self.random.get_number(1, 6)
        die2 = self.random.get_number(1, 6)
        return die1, die2, die1 + die2