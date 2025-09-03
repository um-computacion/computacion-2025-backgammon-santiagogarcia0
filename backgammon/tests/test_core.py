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

class TestPlayer(unittest.TestCase):

    def test_player_initialization(self):
        player = Player("Santiago", 15)
        self.assertEqual(player._Player__name, "Santiago")
        self.assertEqual(player._Player__checkers, 15)

    def test_move_checker_reduces_checkers(self):
        player = Player("Santiago", 5)
        player.move_checker()
        self.assertEqual(player._Player__checkers, 4)

    def test_cannot_move_more_checkers_than_owned(self):
        player = Player("Santiago", 1)
        player.move_checker()
        with self.assertRaises(ValueError):
            player.move_checker()


if __name__ == "__main__":
    unittest.main()