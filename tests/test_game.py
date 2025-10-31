import unittest
from unittest.mock import patch
from backgammon.core.game import Game
from backgammon.core.player import Player

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.player1 = self.game.players[0]
        self.player2 = self.game.players[1]
        self.game.start_game()

    def test_start_game(self):
        self.assertIsNotNone(self.game.board)
        self.assertEqual(len(self.game.players), 2)

    def test_roll_dice_and_no_legal_moves(self):
        # Bloquear todos los movimientos de salida del home de P2
        for i in range(1, 7):
            self.game.board.points[i] = [self.player1.name] * 2
        
        # Poner una ficha de P2 en la barra
        self.game.board.bar[self.player2.name].append(self.player2.name)
        self.game.current_turn_index = 1 # Turno de P2
        
        initial_turn = self.game.current_turn_index
        
        # Simular una tirada que no permite salir de la barra
        with patch.object(self.game.dice, 'roll', return_value=(1, 2)):
            self.game.roll_dice()
        
        # El turno debería cambiar porque no hay movimientos legales
        self.assertNotEqual(initial_turn, self.game.current_turn_index)

    def test_move_consumes_dice(self):
        self.game.available_moves = [3]
        self.game.board.points[24] = [self.player1.name]
        self.game.move(24, 21)
        self.assertEqual(len(self.game.available_moves), 0)

    def test_next_turn(self):
        initial_player = self.game.current_player
        self.game.next_turn()
        self.assertNotEqual(initial_player, self.game.current_player)

    def test_winner_condition(self):
        self.assertIsNone(self.game.winner)
        self.game.board.borne_off[self.player1.name] = [self.player1.name] * 15
        self.assertTrue(self.game.is_finished())
        self.assertEqual(self.game.winner.name, self.player1.name)

if __name__ == '__main__':
    unittest.main()
