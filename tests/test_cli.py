import unittest
from unittest.mock import patch
from backgammon.cli.cli import CLI
from backgammon.core.player import Player
from backgammon.core.game import Game

class TestCLI(unittest.TestCase):
    def setUp(self):
        # Creamos CLI con juego inicializado
        self.cli = CLI()
        player1 = Player("Jugador1")
        player2 = Player("Jugador2")
        self.cli.game = Game(player1, player2)
        self.cli.game.start_game()

    @patch("builtins.input", side_effect=["1"])
    def test_tirar_dados(self, mock_input):
        """Verifica que tirar dados no crashee y actualice available_moves."""
        self.cli.show_menu()
        self.assertTrue(len(self.cli.game.available_moves) in (2,4))

    @patch("builtins.input", side_effect=["3"])
    def test_mostrar_tablero(self, mock_input):
        """Mostrar tablero no debe crashear."""
        self.cli.show_menu()

    @patch("builtins.input", side_effect=["4"])
    def test_salir(self, mock_input):
        with self.assertRaises(SystemExit):
            self.cli.show_menu()

    @patch("builtins.input", side_effect=["2", "24", "23"])
    def test_mover_ficha_valida(self, mock_input):
        """Mueve una ficha válida (preparada) y consume el dado."""
        # preparamos una ficha del jugador actual en 24 (player0)
        self.cli.game.board.points[24] = [self.cli.game.current_player.name]
        self.cli.game.available_moves = [1]
        self.cli.show_menu()
        self.assertEqual(self.cli.game.available_moves, [])

    @patch("builtins.input", side_effect=["2", "24", "22"])
    def test_mover_ficha_invalida(self, mock_input):
        """Movimiento inválido no debe consumir dado."""
        self.cli.game.board.points[24] = [self.cli.game.current_player.name]
        self.cli.game.available_moves = [1]
        self.cli.show_menu()
        self.assertEqual(self.cli.game.available_moves, [1])

    @patch("builtins.input", side_effect=["1"])
    def test_tirar_dados_juego_terminado(self, mock_input):
        """Si juego terminado, tirar dados no hace nada."""
        winner_name = self.cli.game.current_player.name
        self.cli.game.board.borne_off[winner_name] = [winner_name]*15
        self.cli.show_menu()
        self.assertEqual(self.cli.game.available_moves, [])

if __name__ == "__main__":
    unittest.main()
