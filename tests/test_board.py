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
        # Dejamos un punto con 1 ficha de player2
        self.board.points[5] = [self.player2.name]
        # Movemos player1 a ese punto
        self.board.points[1] = [self.player1.name]  # una sola ficha para mover
        moved = self.board.move_checker(self.player1, 1, 5)

        self.assertTrue(moved)
        self.assertIn(self.player2.name, self.board.bar[self.player2.name])
        self.assertIn(self.player1.name, self.board.points[5])

    def test_no_hit_with_multiple_checkers(self):
        """No debe capturar si el punto tiene más de una ficha enemiga."""
        self.board.points[5] = [self.player2.name, self.player2.name]
        self.board.points[1] = [self.player1.name]

        moved = self.board.move_checker(self.player1, 1, 5)

        self.assertTrue(moved)  # puede moverse, pero no golpea
        self.assertEqual(self.board.bar[self.player2.name], [])
        self.assertEqual(self.board.points[5].count(self.player2.name), 2)
        self.assertIn(self.player1.name, self.board.points[5])

if __name__ == "__main__":
    unittest.main()
