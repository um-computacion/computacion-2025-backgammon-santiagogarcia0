import unittest
from backgammon.core.backgammon_game import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game("Santiago", "Ana")

    def test_initial_turn(self):
        """El turno inicial debe ser del primer jugador."""
        self.assertEqual(self.game.current_player.__name__, "Santiago")

    def test_switch_turn(self):
        """El turno debe cambiar al otro jugador."""
        self.game.switch_turn()
        self.assertEqual(self.game.current_player.__name__, "Ana")

    def test_roll_dice(self):
        """La tirada de dados debe dar valores entre 1 y 6."""
        roll = self.game.roll_dice()
        self.assertEqual(len(roll), 2)
        self.assertTrue(all(1 <= value <= 6 for value in roll))
