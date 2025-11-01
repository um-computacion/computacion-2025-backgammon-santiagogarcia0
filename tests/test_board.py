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

    def test_get_legal_moves_bear_off(self):
        # Preparar tablero para bear off
        self.board.points = {i: [] for i in range(1, 25)}
        self.board.points[1] = [self.player1.name]
        self.board.points[3] = [self.player1.name]
        
        # Test de bear off exacto
        moves = self.board.get_legal_moves(self.player1, 1, [1])
        self.assertIn(0, moves)

        # Test de bear off con dado mayor
        moves = self.board.get_legal_moves(self.player1, 3, [4])
        self.assertIn(0, moves)

        # Test de bear off inválido (dado menor)
        moves = self.board.get_legal_moves(self.player1, 3, [2])
        self.assertNotIn(0, moves)

    def test_get_legal_moves_bear_off_white_player(self):
        # Preparar tablero para bear off del jugador blanco
        self.board.points = {i: [] for i in range(1, 25)}
        self.board.points[22] = [self.player2.name]
        self.board.points[24] = [self.player2.name]
        
        # Test de bear off exacto
        moves = self.board.get_legal_moves(self.player2, 24, [1])
        self.assertIn(25, moves)

        # Test de bear off con dado mayor (y checker más lejano)
        moves = self.board.get_legal_moves(self.player2, 24, [3])
        self.assertIn(25, moves)

        # Test de bear off inválido (no es el checker más lejano)
        moves = self.board.get_legal_moves(self.player2, 22, [5])
        self.assertNotIn(25, moves)

if __name__ == '__main__':
    unittest.main()
