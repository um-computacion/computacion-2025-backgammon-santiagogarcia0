"""
Módulo backgammon_game
Coordina la lógica principal del juego de Backgammon.
"""

from .player import Player
from .board import Board
from .dice import Dice


class BackgammonGame:
    """
    Coordina el flujo del juego.
    Maneja jugadores, tablero, dados y turnos.
    """

    def __init__(self, player1_name: str = "Jugador 1", player2_name: str = "Jugador 2"):
        self.__tablero__ = Board()
        self.__dados__ = Dice()
        self.__jugadores__ = [Player(player1_name), Player(player2_name)]
        self.__turno_actual__ = 0  # índice del jugador actual
        self.__tablero__.setup_board(self.__jugadores__)

    @property
    def tablero(self) -> Board:
        """Devuelve el tablero del juego."""
        return self.__tablero__

    @property
    def jugadores(self) -> list:
        """Devuelve la lista de jugadores."""
        return self.__jugadores__

    @property
    def jugador_actual(self) -> Player:
        """Devuelve el jugador que tiene el turno."""
        return self.__jugadores__[self.__turno_actual__]

    def tirar_dados(self):
        """
        Tira los dados y retorna el resultado.
        """
        return self.__dados__.roll()

    def cambiar_turno(self):
        """
        Cambia el turno al otro jugador.
        """
        self.__turno_actual__ = 1 - self.__turno_actual__
