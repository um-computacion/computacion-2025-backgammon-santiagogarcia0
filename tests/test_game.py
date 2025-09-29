import unittest
from backgammon.core.game import Game
from backgammon.core.player import Player

class TestGame(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("Santiago")
        self.player2 = Player("Ana")
        self.game = Game(self.player1, self.player2)
        self.game.start_game()

    def test_initial_turn(self):
        self.assertEqual(self.game.current_player.name, "Santiago")

    def test_switch_turn(self):
        self.game.next_turn()
        self.assertEqual(self.game.current_player.name, "Ana")

    def test_roll_dice(self):
        roll = self.game.roll_dice()
        self.assertEqual(len(roll), 2)
        self.assertTrue(all(1 <= value <= 6 for value in roll))

    def test_game_finished(self):
        self.game.board.borne_off[self.player1.name] = [self.player1.name] * 15
        self.assertTrue(self.game.is_finished())

if __name__ == "__main__":
    unittest.main()
