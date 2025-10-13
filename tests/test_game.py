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
        self.game.next_turn()
        self.assertEqual(self.game.current_player.name, "Santiago")

    def test_roll_dice(self):
        roll = self.game.roll_dice()
        self.assertEqual(len(roll), 2)
        self.assertTrue(all(1 <= value <= 6 for value in roll))
        # test dobles
        self.game.dice.roll = lambda: (3, 3)
        roll = self.game.roll_dice()
        self.assertEqual(self.game.available_moves, [3, 3, 3, 3])

    def test_move_consumes_dice_and_switch_turn(self):
        self.game.available_moves = [2, 3]
        self.game.board.points[1] = [self.player1.name]
        moved = self.game.move(1, 3)  # usa el dado 2
        self.assertTrue(moved)
        self.assertEqual(self.game.available_moves, [3])
        # siguiente movimiento consume último dado y cambia turno
        self.game.board.points[3] = [self.player1.name]
        moved2 = self.game.move(3, 6)
        self.assertTrue(moved2)
        self.assertEqual(self.game.current_player.name, "Ana")
        self.assertEqual(self.game.available_moves, [])

    def test_move_no_available_moves_skips_turn(self):
        # ninguna jugada posible
        self.game.available_moves = [6]
        # poner bloque para el jugador 1
        self.game.board.points[1] = [self.player1.name]
        self.game.board.points[7] = [self.player2.name, self.player2.name]
        moved = self.game.move(1, 7)
        self.assertFalse(moved)
        self.assertEqual(self.game.current_player.name, "Ana")

    def test_game_finished(self):
        self.game.board.borne_off[self.player1.name] = [self.player1.name] * 15
        self.assertTrue(self.game.is_finished())
        winner = self.game.check_winner()
        self.assertEqual(winner.name, "Santiago")

if __name__ == "__main__":
    unittest.main()
