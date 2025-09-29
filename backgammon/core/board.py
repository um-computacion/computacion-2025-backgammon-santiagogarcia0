"""
Módulo board
Contiene la clase Board que representa el tablero de Backgammon.
"""

class Board:
    """
    Representa el tablero del juego.
    Administra las posiciones de las fichas, bar y borneado.
    """

    def __init__(self):
        self.points = {i: [] for i in range(1, 25)}
        self._initialize_checkers()
        self.bar = {}
        self.borne_off = {}

    def _initialize_checkers(self):
        """Coloca fichas iniciales (ejemplo simplificado)."""
        self.points[1] = ['B'] * 2
        self.points[12] = ['B'] * 5
        self.points[17] = ['B'] * 3
        self.points[19] = ['B'] * 5

        self.points[24] = ['W'] * 2
        self.points[13] = ['W'] * 5
        self.points[8] = ['W'] * 3
        self.points[6] = ['W'] * 5

    def setup_board(self, players):
        """Configura el tablero inicial con 15 fichas por jugador."""
        self.points[1] = [players[0].name] * 15
        self.points[24] = [players[1].name] * 15
        self.bar = {p.name: [] for p in players}
        self.borne_off = {p.name: [] for p in players}

    def _valid_point(self, point):
        """Devuelve True si el punto está dentro del rango permitido."""
        return 0 <= point <= 25

    def _remove_checker(self, player, from_point):
        """Quita una ficha de un punto."""
        self.points[from_point].remove(player.name)

    def _add_checker(self, player, to_point):
        """Agrega una ficha a un punto."""
        self.points[to_point].append(player.name)

    def can_move(self, player, from_point, to_point, dice_rolls):
        """Valida si el movimiento es legal según reglas básicas y dados."""
        if not self._valid_point(from_point) or not self._valid_point(to_point):
            return False
        if not self.points[from_point] or self.points[from_point][0] != player.name:
            return False

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
        if to_point in (0, 25):
            self._remove_checker(player, from_point)
            self.borne_off[player.name].append(player.name)
            return True

        # Golpe (hit)
        if (
            self.points[to_point]
            and self.points[to_point][0] != player.name
            and len(self.points[to_point]) == 1
        ):
            opponent = self.points[to_point].pop()
            self.bar[opponent].append(opponent)

        # Movimiento normal
        self._remove_checker(player, from_point)
        self._add_checker(player, to_point)
        return True

    def __str__(self):
        """Representación simplificada del tablero."""
        lines = [f"{i}: {self.points[i]}" for i in range(1, 25)]
        return "\n".join(lines)
