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
        """El tablero debe tener 15 fichas de cada jugador en posiciones iniciales."""
        self.assertEqual(len(self.board._Board__points__[1]), 15)
        self.assertEqual(len(self.board._Board__points__[24]), 15)

    def test_valid_move(self):
        """Debe poder mover una ficha si el movimiento es válido."""
        moved = self.board.move_checker(self.player1, 1, 2)
        self.assertTrue(moved)
        self.assertIn(self.player1.__name__, self.board._Board__points__[2])

    def test_invalid_move(self):
        """No debe permitir mover una ficha de una posición vacía."""
        moved = self.board.move_checker(self.player1, 5, 6)
        self.assertFalse(moved)
