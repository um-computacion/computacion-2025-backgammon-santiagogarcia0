import unittest
from unittest.mock import MagicMock, patch
from backgammon.cli.cli import CLI


class TestCLI(unittest.TestCase):
    def setUp(self):
        # Creamos un mock de Game
        self.mock_game = MagicMock()
        self.mock_game.board = "TABLERO_MOCK"

        # Instanciamos la CLI con el mock de game
        self.cli = CLI(self.mock_game)

    @patch("builtins.print")
    def test_show_message(self, mock_print):
        self.cli.show_message("Hola")
        mock_print.assert_called_once_with("Hola")

    @patch("builtins.print")
    def test_show_board(self, mock_print):
        self.cli.show_board()
        mock_print.assert_any_call("TABLERO_MOCK")

    @patch("builtins.print")
    def test_show_dice(self, mock_print):
        self.cli.show_dice([3, 5])
        mock_print.assert_called_once_with("Dados: [3, 5]")

    @patch("builtins.input", return_value="6 3")
    def test_ask_move(self, mock_input):
        movimiento = self.cli.ask_move()
        self.assertEqual(movimiento, "6 3")
        mock_input.assert_called_once_with("Ingresa tu movimiento (ej: '6 3'): ")

    @patch("builtins.print")
    def test_show_winner(self, mock_print):
        mock_player = MagicMock()
        mock_player.name = "Jugador1"
        self.cli.show_winner(mock_player)
        mock_print.assert_called_once_with("¡Jugador1 ha ganado el juego!")

    @patch("builtins.print")
    def test_start(self, mock_print):
        """
        start() debe mostrar el mensaje de bienvenida y el tablero.
        """
        self.cli.start()
        mock_print.assert_any_call("Bienvenido a Backgammon!")
        mock_print.assert_any_call("TABLERO_MOCK")


if __name__ == "__main__":
    unittest.main()
