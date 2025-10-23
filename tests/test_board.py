import unittest
from backgammon.core.board import Board
from backgammon.core.player import Player

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = Player("Santiago")  # player0: direction -1 (24 -> 1)
        self.player2 = Player("Ana")       # player1: direction +1 (1 -> 24)
        self.board.setup_board([self.player1, self.player2])

    def test_valid_move_to_empty_point(self):
        # preparo una ficha suelta para mover (no importa el punto de inicio real)
        self.board.points[24] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 24, 23, [1])
        self.assertTrue(moved)

    def test_invalid_move_with_wrong_dice(self):
        self.board.points[24] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 24, 22, [1])  # distancia 2 pero dado 1
        self.assertFalse(moved)

    def test_invalid_move_to_blocked_point(self):
        # bloqueamos punto 23 con 2 fichas enemigas
        self.board.points[23] = [self.player2.name, self.player2.name]
        self.board.points[24] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 24, 23, [1])
        self.assertFalse(moved)

    def test_hit_single_checker(self):
        # dejar una ficha enemiga en 23, mover desde 24 a 23 con dice 1
        self.board.points[23] = [self.player2.name]
        self.board.points[24] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 24, 23, [1])
        self.assertTrue(moved)
        self.assertIn(self.player2.name, self.board.bar[self.player2.name])

    def test_no_hit_with_multiple_checkers(self):
        self.board.points[23] = [self.player2.name, self.player2.name]
        self.board.points[24] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 24, 23, [1])
        # movimiento válido (se agrega la ficha propia) pero no golpea
        self.assertTrue(moved)
        self.assertEqual(self.board.bar[self.player2.name], [])

    def test_multiple_hits_in_sequence(self):
        # dos puntos con ficha enemiga en 23 y 22; mover 24->23 (1), luego 23->22 (1)
        self.board.points[23] = [self.player2.name]
        self.board.points[22] = [self.player2.name]
        self.board.points[24] = [self.player1.name]
        moved1 = self.board.move_checker(self.player1, 24, 23, [1,1])
        moved2 = self.board.move_checker(self.player1, 23, 22, [1])
        self.assertTrue(moved1)
        self.assertTrue(moved2)
        self.assertIn(self.player2.name, self.board.bar[self.player2.name])

    def test_bear_off(self):
        # Para player1 (direction -1) borne off desde 1 -> 0 con dado 1,
        # aseguramos que todas sus fichas estén en home (1..6)
        # colocamos única ficha en 1 y ninguna fuera del home
        self.board.points = {i: [] for i in range(1, 25)}
        self.board.points[1] = [self.player1.name]
        # clear other player's checkers to avoid interferencia
        self.board.bar = {self.player1.name: [], self.player2.name: []}
        self.board.borne_off = {self.player1.name: [], self.player2.name: []}
        moved = self.board.move_checker(self.player1, 1, 0, [1])
        self.assertTrue(moved)
        self.assertIn(self.player1.name, self.board.borne_off[self.player1.name])

    def test_invalid_bear_off_when_not_in_home(self):
        # ficha fuera del home (por ejemplo en 10) no permite borne off
        self.board.points[10] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 10, 0, [10])
        self.assertFalse(moved)
        self.assertNotIn(self.player1.name, self.board.borne_off[self.player1.name])

if __name__ == "__main__":
    unittest.main()
