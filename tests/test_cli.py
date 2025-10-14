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
        """Verifica que tirar dados no crashee y devuelva 2 valores."""
        self.cli.show_menu()
        self.assertTrue(len(self.cli.game.available_moves) in [2,4])  # normales o dobles

    @patch("builtins.input", side_effect=["3"])
    def test_mostrar_tablero(self, mock_input):
        """Verifica que mostrar tablero no crashee."""
        self.cli.show_menu()  # solo imprime estado del tablero

    @patch("builtins.input", side_effect=["4"])
    def test_salir(self, mock_input):
        """Verifica que la opción salir lance SystemExit."""
        with self.assertRaises(SystemExit):
            self.cli.show_menu()

    @patch("builtins.input", side_effect=["2", "1", "3"])
    def test_mover_ficha_valida(self, mock_input):
        """Verifica que se pueda mover una ficha válida."""
        # Ajustamos tablero para un movimiento válido
        self.cli.game.board.points[1] = [self.cli.game.current_player.name]
        self.cli.game.available_moves = [2]
        self.cli.show_menu()
        # Si se movió, debería consumir el dado
        self.assertEqual(self.cli.game.available_moves, [])

    @patch("builtins.input", side_effect=["2", "1", "5"])
    def test_mover_ficha_invalida(self, mock_input):
        """Verifica que un movimiento inválido no cambie available_moves."""
        self.cli.game.board.points[1] = [self.cli.game.current_player.name]
        self.cli.game.available_moves = [2]
        self.cli.show_menu()
        # Movimiento inválido → dado no consumido
        self.assertEqual(self.cli.game.available_moves, [2])

    @patch("builtins.input", side_effect=["1"])
    def test_tirar_dados_juego_terminado(self, mock_input):
        """Verifica que no se puedan tirar dados si el juego terminó."""
        # Forzamos victoria
        winner_name = self.cli.game.current_player.name
        self.cli.game.board.borne_off[winner_name] = [winner_name]*15
        self.cli.show_menu()
        # available_moves debería seguir vacío
        self.assertEqual(self.cli.game.available_moves, [])

if __name__ == "__main__":
    unittest.main()
