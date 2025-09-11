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
        self.__initialize_checkers__()

    def __initialize_checkers__(self):
        """Coloca las fichas en posiciones iniciales estándar (simplificado)."""
        # Posiciones iniciales de ejemplo: dos jugadores B y W
        self.__points__[1] = ['B'] * 2
        self.__points__[12] = ['B'] * 5
        self.__points__[17] = ['B'] * 3
        self.__points__[19] = ['B'] * 5

        self.__points__[24] = ['W'] * 2
        self.__points__[13] = ['W'] * 5
        self.__points__[8] = ['W'] * 3
        self.__points__[6] = ['W'] * 5

    def setup_board(self, players):
        """
        Asocia fichas con los nombres de los jugadores (simplificado):
        - Jugador 1 en la posición 1
        - Jugador 2 en la posición 24
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

    def __str__(self):
        """Representación simplificada del tablero."""
        board_str = ""
        for i in range(1, 25):
            board_str += f"{i}: {self.__points__[i]}\n"
        return board_str
