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
        self.bar = {}
        self.borne_off = {}

    def _initialize_checkers(self):
        self.points[1] = ['B'] * 2
        self.points[12] = ['B'] * 5
        self.points[17] = ['B'] * 3
        self.points[19] = ['B'] * 5

        self.points[24] = ['W'] * 2
        self.points[13] = ['W'] * 5
        self.points[8] = ['W'] * 3
        self.points[6] = ['W'] * 5

    def setup_board(self, players):
        self.points[1] = [players[0].name] * 15
        self.points[24] = [players[1].name] * 15
        self.bar = {players[0].name: [], players[1].name: []}
        self.borne_off = {players[0].name: [], players[1].name: []}

    def can_move(self, player, from_point, to_point, dice_rolls):
        """Valida si el movimiento es legal según las reglas básicas y dados."""
        if from_point < 1 or from_point > 24:
            return False
        if to_point < 0 or to_point > 25:
            return False
        if not self.points[from_point] or self.points[from_point][0] != player.name:
            return False

        # Validar distancia con dados
        distance = abs(to_point - from_point)
        if distance not in dice_rolls and to_point not in (0, 25):
            return False

        return True

    def move_checker(self, player, from_point, to_point, dice_rolls):
        """Mueve ficha si el movimiento es válido con los dados disponibles."""
        if not self.can_move(player, from_point, to_point, dice_rolls):
            return False

        distance = abs(to_point - from_point)
        if distance in dice_rolls:
            dice_rolls.remove(distance)

        # Borneado
        if to_point == 0 or to_point == 25:
            self.points[from_point].remove(player.name)
            self.borne_off[player.name].append(player.name)
            return True

        # Golpe (hit)
        if self.points[to_point] and self.points[to_point][0] != player.name and len(self.points[to_point]) == 1:
            opponent = self.points[to_point][0]
            captured = self.points[to_point].pop()
            self.bar[opponent].append(captured)

        # Movimiento normal
        self.points[from_point].remove(player.name)
        self.points[to_point].append(player.name)
        return True

    def __str__(self):
        board_str = ""
        for i in range(1, 25):
            board_str += f"{i}: {self.points[i]}\n"
        return board_str
