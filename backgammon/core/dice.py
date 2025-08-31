import random

class Dice:

    """Representa los dados utilizados en Backgammon."""

    def roll(self):

        return random.randint(1, 6), random.randint(1, 6)
