import unittest
from backgammon.core.board import Board
from backgammon.core.player import Player

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = Player("P1")
        self.player2 = Player("P2")
        self.board.setup_board([self.player1, self.player2])

    def test_valid_move_to_empty_point(self):
        self.board.points[24] = [self.player1.name]
        moves = self.board.get_legal_moves(self.player1, 24, [1])
        self.assertIn(23, moves)

    def test_invalid_move_to_blocked_point(self):
        self.board.points[23] = [self.player2.name, self.player2.name]
        self.board.points[24] = [self.player1.name]
        moves = self.board.get_legal_moves(self.player1, 24, [1])
        self.assertNotIn(23, moves)

    def test_hit_single_checker(self):
        self.board.points[23] = [self.player2.name]
        self.board.points[24] = [self.player1.name]
        self.board.move_checker(self.player1, 24, 23)
        self.assertIn(self.player2.name, self.board.bar[self.player2.name])
        self.assertEqual(self.board.points[23], [self.player1.name])

    def test_bear_off(self):
        # Preparar tablero para bear off
        self.board.points = {i: [] for i in range(1, 25)}
        self.board.points[1] = [self.player1.name]
        self.board.move_checker(self.player1, 1, 0)
        self.assertIn(self.player1.name, self.board.borne_off[self.player1.name])

    def test_invalid_bear_off_when_not_in_home(self):
        self.board.points = {i: [] for i in range(1, 25)}
        self.board.points[7] = [self.player1.name] # Ficha fuera del home
        self.board.points[1] = [self.player1.name]
        moves = self.board.get_legal_moves(self.player1, 1, [1])
        self.assertNotIn(0, moves)

if __name__ == '__main__':
    unittest.main()
