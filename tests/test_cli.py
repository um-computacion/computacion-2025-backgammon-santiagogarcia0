import unittest
from unittest.mock import patch, PropertyMock
from backgammon.cli.cli import CLI

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.cli = CLI()

    @patch('builtins.input', side_effect=[''])
    @patch('builtins.print')
    def test_start_game_flow_runs(self, mock_print, mock_input):
        # Simular que el juego termina y hay un ganador
        with patch.object(self.cli.game, 'is_finished', return_value=True):
            with patch('backgammon.core.game.Game.winner', new_callable=PropertyMock) as mock_winner:
                mock_winner.return_value = self.cli.game.players[0]
                self.cli.start()
        
        # Verificar que se anuncia al ganador
        mock_print.assert_any_call(f"\n¡Felicidades, {self.cli.game.players[0].name}! Has ganado. 🏆")

    @patch('builtins.print')
    def test_print_board_state(self, mock_print):
        self.cli.print_board_state()
        mock_print.assert_any_call("="*40)

if __name__ == '__main__':
    unittest.main()
