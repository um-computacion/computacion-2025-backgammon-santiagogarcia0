import unittest
from unittest.mock import patch
from backgammon.cli.cli import CLI
from backgammon.core.player import Player
from backgammon.core.backgammon_game import BackgammonGame


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.cli = CLI()
        player1 = Player("Jugador1")
        player2 = Player("Jugador2")
        self.cli.game = BackgammonGame([player1, player2])

    @patch("builtins.input", side_effect=["1"])
    def test_tirar_dados(self, mock_input):
        # Llamamos a show_menu y verificamos que no crashea
        self.cli.show_menu()

    @patch("builtins.input", side_effect=["3"])
    def test_mostrar_tablero(self, mock_input):
        self.cli.show_menu()

    @patch("builtins.input", side_effect=["4"])
    def test_salir(self, mock_input):
        with self.assertRaises(SystemExit):
            self.cli.show_menu()
