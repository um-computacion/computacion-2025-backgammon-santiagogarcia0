import unittest
from backgammon.core.board import Board
from backgammon.core.player import Player

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = Player("Santiago")
        self.player2 = Player("Ana")
        self.board.setup_board([self.player1, self.player2])

    def test_hit_single_checker(self):
        """Debe capturar una ficha solitaria del oponente (hit)."""
        self.board.points[5] = [self.player2.name]
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 5, [4])
        self.assertTrue(moved)
        self.assertIn(self.player2.name, self.board.bar[self.player2.name])
        self.assertIn(self.player1.name, self.board.points[5])

    def test_no_hit_with_multiple_checkers(self):
        """No debe capturar si el punto tiene más de una ficha enemiga."""
        self.board.points[5] = [self.player2.name, self.player2.name]
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 5, [4])
        self.assertTrue(moved)
        self.assertEqual(self.board.bar[self.player2.name], [])
        self.assertEqual(self.board.points[5].count(self.player2.name), 2)
        self.assertIn(self.player1.name, self.board.points[5])

    def test_bear_off(self):
        """Debe permitir borneado de fichas."""
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 0, [1])
        self.assertTrue(moved)
        self.assertIn(self.player1.name, self.board.borne_off[self.player1.name])

    def test_illegal_move_wrong_dice(self):
        """No debe permitir movimiento si no coincide con el dado."""
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 4, [6])
        self.assertFalse(moved)

if __name__ == "__main__":
    unittest.main()
