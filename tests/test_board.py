import unittest
from backgammon.core.board import Board
from backgammon.core.player import Player

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = Player("Santiago")
        self.player2 = Player("Ana")
        self.board.setup_board([self.player1, self.player2])

    def test_initial_setup(self):
        self.assertEqual(len(self.board.points[1]), 15)
        self.assertEqual(len(self.board.points[24]), 15)
        self.assertIn(self.player1.name, self.board.bar)
        self.assertIn(self.player1.name, self.board.borne_off)

    def test_bear_off_checker(self):
        """Debe permitir borneado (sacar fichas del tablero)."""
        moved = self.board.move_checker(self.player1, 1, 0)  # borneado
        self.assertTrue(moved)
        self.assertIn(self.player1.name, self.board.borne_off[self.player1.name])

    def test_bar_starts_empty(self):
        """Al inicio, el bar debe estar vacío."""
        self.assertEqual(self.board.bar[self.player1.name], [])
        self.assertEqual(self.board.bar[self.player2.name], [])

if __name__ == "__main__":
    unittest.main()
