import unittest
from backgammon.core.dice import Dice
from backgammon.core.player import Player


class TestDice(unittest.TestCase):

    def test_roll_in_range(self):
        dice = Dice()
        value = dice.roll()
        self.assertIn(value, range(1, 7))

    def test_roll_double_in_range(self):
        dice = Dice()
        roll1, roll2 = dice.roll_double()
        self.assertIn(roll1, range(1, 7))
        self.assertIn(roll2, range(1, 7))

    def test_last_roll_updates(self):
        dice = Dice()
        dice.roll()
        self.assertIsNotNone(dice._Dice__last_roll)  # atributo privado con name mangling