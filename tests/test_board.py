import unittest
from backgammon.core.board import Board
from backgammon.core.player import Player

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = Player("Santiago")
        self.player2 = Player("Ana")
        self.board.setup_board([self.player1, self.player2])

    def test_valid_move_to_empty_point(self):
        """Debe permitir mover una ficha a un punto vacío."""
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 3, [2])
        self.assertTrue(moved)
        self.assertIn(self.player1.name, self.board.points[3])

    def test_invalid_move_with_wrong_dice(self):
        """No debe permitir mover si no coincide con la tirada."""
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 4, [2])
        self.assertFalse(moved)
        self.assertNotIn(self.player1.name, self.board.points[4])

    def test_invalid_move_to_blocked_point(self):
        """No debe permitir mover a un punto con 2+ fichas enemigas."""
        self.board.points[4] = [self.player2.name, self.player2.name]
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 4, [3])
        self.assertFalse(moved)
        self.assertIn(self.player1.name, self.board.points[1])

if __name__ == "__main__":
    unittest.main()
