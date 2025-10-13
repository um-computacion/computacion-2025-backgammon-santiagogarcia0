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
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 3, [2])
        self.assertTrue(moved)

    def test_invalid_move_with_wrong_dice(self):
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 4, [2])
        self.assertFalse(moved)

    def test_invalid_move_to_blocked_point(self):
        self.board.points[4] = [self.player2.name, self.player2.name]
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 4, [3])
        self.assertFalse(moved)

    def test_hit_single_checker(self):
        self.board.points[5] = [self.player2.name]
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 5, [4])
        self.assertTrue(moved)
        self.assertIn(self.player2.name, self.board.bar[self.player2.name])

    def test_no_hit_with_multiple_checkers(self):
        self.board.points[5] = [self.player2.name, self.player2.name]
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 5, [4])
        self.assertTrue(moved)

    def test_multiple_hits_in_sequence(self):
        self.board.points[5] = [self.player2.name]
        self.board.points[6] = [self.player2.name]
        self.board.points[1] = [self.player1.name]
        moved1 = self.board.move_checker(self.player1, 1, 5, [4])
        moved2 = self.board.move_checker(self.player1, 5, 6, [1])
        self.assertTrue(moved1)
        self.assertTrue(moved2)
        self.assertIn(self.player2.name, self.board.bar[self.player2.name])

    def test_bear_off(self):
        self.board.points[1] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 1, 0, [1])
        self.assertTrue(moved)
        self.assertIn(self.player1.name, self.board.borne_off[self.player1.name])

    def test_invalid_bear_off_when_not_in_home(self):
        self.board.points[10] = [self.player1.name]
        moved = self.board.move_checker(self.player1, 10, 0, [10])
        self.assertFalse(moved)
        self.assertNotIn(self.player1.name, self.board.borne_off[self.player1.name])

if __name__ == "__main__":
    unittest.main()
