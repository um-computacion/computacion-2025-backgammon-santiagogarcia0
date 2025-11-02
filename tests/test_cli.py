import unittest
from unittest.mock import patch, PropertyMock
from backgammon.cli.cli import CLI
from backgammon.core.player import Player

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.cli = CLI()

    @patch('builtins.input', side_effect=['24', '23'])
    def test_get_player_move_valid(self, mock_input):
        from_point, to_point = self.cli._get_player_move()
        self.assertEqual(from_point, 24)
        self.assertEqual(to_point, 23)

    @patch('builtins.input', side_effect=['bar', '22'])
    def test_get_player_move_bar(self, mock_input):
        from_point, to_point = self.cli._get_player_move()
        self.assertEqual(from_point, 'bar')
        self.assertEqual(to_point, 22)

    @patch('builtins.input', side_effect=['invalid', '23'])
    @patch('builtins.print')
    def test_get_player_move_invalid(self, mock_print, mock_input):
        from_point, to_point = self.cli._get_player_move()
        self.assertIsNone(from_point)
        self.assertIsNone(to_point)
        mock_print.assert_called_with("Entrada inválida. Introduce números para los puntos.")

    @patch('builtins.input', side_effect=['']) # For the initial "Press Enter"
    @patch('builtins.print')
    @patch('backgammon.core.dice.Dice.roll', return_value=(1, 2))
    @patch('backgammon.cli.cli.CLI._get_player_move', side_effect=[(24, 23), (24, 22)])
    @patch('backgammon.core.game.Game.winner', new_callable=PropertyMock, return_value=Player("Jugador 1"))
    @patch('backgammon.core.game.Game.is_finished', side_effect=[False, False, False, False, True])
    def test_start_happy_path(self, mock_is_finished, mock_winner, mock_get_move, mock_roll, mock_print, mock_input):
        self.cli.start()
        mock_print.assert_any_call("Movimiento realizado con éxito. ✅")
        self.assertEqual(mock_get_move.call_count, 2)

    @patch('builtins.input', side_effect=[''])
    @patch('builtins.print')
    @patch('backgammon.core.dice.Dice.roll', return_value=(1, 2))
    @patch('backgammon.core.game.Game.winner', new_callable=PropertyMock, return_value=Player("Jugador 1"))
    @patch('backgammon.core.game.Game.is_finished', side_effect=[False, False, True])
    def test_start_no_legal_moves(self, mock_is_finished, mock_winner, mock_roll, mock_print, mock_input):
        with patch.object(self.cli.game.board, 'has_any_legal_move', return_value=False):
            self.cli.start()
        mock_print.assert_any_call("No tienes movimientos posibles. Pasando turno.")

    @patch('builtins.input', side_effect=[''])
    @patch('builtins.print')
    @patch('backgammon.core.dice.Dice.roll', return_value=(1, 2))
    @patch('backgammon.cli.cli.CLI._get_player_move', side_effect=[(None, None), (24, 23), (24, 22)])
    @patch('backgammon.core.game.Game.winner', new_callable=PropertyMock, return_value=Player("Jugador 1"))
    @patch('backgammon.core.game.Game.is_finished', side_effect=[False, False, False, False, True])
    def test_start_invalid_move_continue(self, mock_is_finished, mock_winner, mock_get_move, mock_roll, mock_print, mock_input):
        self.cli.start()
        self.assertEqual(mock_get_move.call_count, 3)

    @patch('builtins.input', side_effect=[''])
    @patch('builtins.print')
    @patch('backgammon.core.dice.Dice.roll', return_value=(1, 2))
    @patch('backgammon.cli.cli.CLI._get_player_move', side_effect=[(24, 20), (24, 23), (24, 22)])
    @patch('backgammon.core.game.Game.winner', new_callable=PropertyMock, return_value=Player("Jugador 1"))
    @patch('backgammon.core.game.Game.is_finished', side_effect=[False, False, False, False, False, True])
    def test_start_invalid_move_message(self, mock_is_finished, mock_winner, mock_get_move, mock_roll, mock_print, mock_input):
        self.cli.start()
        mock_print.assert_any_call("Movimiento inválido. Inténtalo de nuevo. ❌")
        # The test will exit after the first turn, so we expect 3 calls to get_player_move
        self.assertEqual(mock_get_move.call_count, 3)

if __name__ == '__main__':
    unittest.main()