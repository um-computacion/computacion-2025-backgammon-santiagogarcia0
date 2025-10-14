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

    def test_roll_dice(self):
        roll = self.game.roll_dice()
        self.assertEqual(len(roll), 2)
        self.assertTrue(all(1 <= v <= 6 for v in roll))

    def test_game_finished(self):
        self.game.board.borne_off[self.player1.name] = [self.player1.name]*15
        self.assertTrue(self.game.is_finished())

    def test_move_without_dice(self):
        """No se puede mover si no se lanzaron dados."""
        moved = self.game.move(1, 2)
        self.assertFalse(moved)

    def test_move_after_game_finished(self):
        """No se puede mover si el juego ya terminó."""
        self.game.board.borne_off[self.player1.name] = [self.player1.name]*15
        self.game.available_moves = [1,2]
        moved = self.game.move(1,2)
        self.assertFalse(moved)

    def test_move_no_legal_moves(self):
        """Si no hay movimientos legales, se pasa el turno automáticamente."""
        self.game.available_moves = [6]  # asumiendo que no hay ficha a 6 de distancia
        # bloqueamos todas las fichas de player1
        for i in range(1,25):
            self.game.board.points[i] = [self.player2.name]*2
        prev_turn = self.game.current_turn_index
        moved = self.game.move(1,7)
        self.assertFalse(moved)
        # turno debe pasar
        self.assertNotEqual(self.game.current_turn_index, prev_turn)

if __name__ == "__main__":
    unittest.main()
