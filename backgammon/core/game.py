"""
Módulo game
Contiene la clase Game que gestiona el flujo principal del juego.
"""

from core.board import Board
from core.player import Player
from core.dice import Dice

class Game:
    """
    Representa el juego de Backgammon.
    Controla los jugadores, el tablero y el flujo de turnos.
    """

    def __init__(self):
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__players__ = [Player("Jugador 1"), Player("Jugador 2")]
        self.__current_turn__ = 0  # índice del jugador actual

    def start_game(self):
        """Inicializa el tablero con fichas de ambos jugadores."""
        self.__board__.setup_board(self.__players__)

    def roll_dice(self):
        """Lanza los dados y retorna los valores obtenidos."""
        return self.__dice__.roll()

    def next_turn(self):
        """Cambia el turno al siguiente jugador."""
        self.__current_turn__ = (self.__current_turn__ + 1) % len(self.__players__)

    def get_current_player(self):
        """Devuelve el jugador que tiene el turno actual."""
        return self.__players__[self.__current_turn__]

    def is_finished(self):
        """Determina si el juego terminó (un jugador se quedó sin fichas)."""
        return any(player.has_won() for player in self.__players__)
