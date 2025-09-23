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
        self.points = {i: [] for i in range(1, 25)}
        self._initialize_checkers()

    def _initialize_checkers(self):
        """Coloca las fichas en posiciones iniciales estándar (simplificado)."""
        # Posiciones iniciales de ejemplo: dos jugadores B y W
        self.points[1] = ['B'] * 2
        self.points[12] = ['B'] * 5
        self.points[17] = ['B'] * 3
        self.points[19] = ['B'] * 5

        self.points[24] = ['W'] * 2
        self.points[13] = ['W'] * 5
        self.points[8] = ['W'] * 3
        self.points[6] = ['W'] * 5

    def setup_board(self, players):
        """
        Asocia fichas con los nombres de los jugadores:
        - Jugador 1 en la posición 1
        - Jugador 2 en la posición 24
        """
        self.points[1] = [players[0].name] * 15
        self.points[24] = [players[1].name] * 15

    def can_move(self, player, from_point, to_point):
        """
        Verifica si un movimiento es legal de manera básica.
        - El origen debe tener fichas del jugador.
        - El destino debe estar dentro del rango 1–24.
        """
        if from_point < 1 or from_point > 24:
            return False
        if to_point < 1 or to_point > 24:
            return False
        if not self.points[from_point] or self.points[from_point][0] != player.name:
            return False
        return True

    def move_checker(self, player, from_point, to_point):
        """Mueve una ficha si el movimiento es válido."""
        if not self.can_move(player, from_point, to_point):
            return False
        self.points[from_point].remove(player.name)
        self.points[to_point].append(player.name)
        return True

    def __str__(self):
        """Representación simplificada del tablero."""
        board_str = ""
        for i in range(1, 25):
            board_str += f"{i}: {self.points[i]}\n"
        return board_str
