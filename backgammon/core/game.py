"""
Módulo game
Contiene la clase Game que gestiona el flujo principal del juego.
"""

from backgammon.core.board import Board
from backgammon.core.player import Player
from backgammon.core.dice import Dice

class Game:
    """
    Representa el juego de Backgammon.
    Controla los jugadores, el tablero y el flujo de turnos.
    """

    def __init__(self, player1=None, player2=None):
        self.board = Board()
        self.dice = Dice()
        self.players = [
            player1 if player1 else Player("Jugador 1"),
            player2 if player2 else Player("Jugador 2")
        ]
        self.current_turn_index = 0

    def start_game(self):
        """Inicializa el tablero con fichas de ambos jugadores."""
        self.board.setup_board(self.players)

    def roll_dice(self):
        """Lanza los dados y retorna los valores obtenidos."""
        return self.dice.roll()

    def next_turn(self):
        """Cambia el turno al siguiente jugador."""
        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)

    @property
    def current_player(self):
        """Devuelve el jugador que tiene el turno actual."""
        return self.players[self.current_turn_index]

    def is_finished(self):
        """Determina si el juego terminó (un jugador se quedó sin fichas)."""
        return any(player.has_won() for player in self.players)
