"""
Módulo board
Contiene la clase Board que representa el tablero de Backgammon.
"""

class Board:
    """
    Representa el tablero del juego.
    Administra las posiciones de las fichas.
    """

    def __init__(self):
        self.__points__ = {i: [] for i in range(1, 25)}

    def setup_board(self, players):
        """
        Coloca a los jugadores en un estado inicial simplificado:
        - Jugador 1 con 15 fichas en la posición 1.
        - Jugador 2 con 15 fichas en la posición 24.
        """
        self.__points__[1] = [players[0].__name__] * 15
        self.__points__[24] = [players[1].__name__] * 15

    def move_checker(self, player, from_point, to_point):
        """
        Mueve una ficha de un punto a otro si es válido.
        """
        if self.is_valid_move(player, from_point, to_point):
            self.__points__[from_point].remove(player.__name__)
            self.__points__[to_point].append(player.__name__)
            return True
        return False

    def is_valid_move(self, player, from_point, to_point):
        """Valida un movimiento de manera simplificada."""
        return player.__name__ in self.__points__[from_point]
