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
        # puntos 1..24
        self.points = {i: [] for i in range(1, 25)}
        self._initialize_checkers()
        self.bar = {}        # dict: player_name -> list of captured checkers
        self.borne_off = {}  # dict: player_name -> list of borne-off checkers

    def _initialize_checkers(self):
        """Coloca fichas iniciales de ejemplo (solo si no se llamó setup_board)."""
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
        Configura el tablero inicial con 15 fichas por jugador en posiciones estándar
        y establece dirección de movimiento para cada jugador (estándar):
            - players[0] starts at point 24 and moves toward 1  (direction = -1)
            - players[1] starts at point 1  and moves toward 24 (direction = +1)
        También inicializa bar y borne_off.
        """
        # limpiar y colocar todos en puntos de prueba (simplificado)
        self.points = {i: [] for i in range(1, 25)}
        # estándar: player0 en 24, player1 en 1
        self.points[24] = [players[0].name] * 15
        self.points[1] = [players[1].name] * 15

        # Inicializar estructuras
        self.bar = {p.name: [] for p in players}
        self.borne_off = {p.name: [] for p in players}

        # Asignar dirección (player0: -1, player1: +1)
        try:
            players[0].direction = -1
            players[1].direction = +1
        except Exception:
            pass

    def _valid_point(self, point):
        """Valida puntos permitidos (incluidos 0 y 25 para borne off)."""
        return 0 <= point <= 25

    def _remove_checker(self, player, from_point):
        """Quita una ficha de un punto."""
        self.points[from_point].remove(player.name)

    def _add_checker(self, player, to_point):
        """Agrega una ficha a un punto."""
        self.points[to_point].append(player.name)

    def _entry_point_from_bar(self, player, dice_value):
        """
        Calcula punto de entrada desde la barra según jugador y dado.
        - direction +1 (player que va 1->24): entry = dice_value (1..6)
        - direction -1 (player que va 24->1): entry = 25 - dice_value (24..19)
        """
        direction = getattr(player, "direction", +1)
        if direction == +1:
            return dice_value
        else:
            return 25 - dice_value

    def _in_home_board(self, player, point):
        """
        Verifica si un punto pertenece al 'home' del jugador:
        - direction +1: home = 19..24
        - direction -1: home = 1..6
        """
        direction = getattr(player, "direction", +1)
        if direction == +1:
            return 19 <= point <= 24
        else:
            return 1 <= point <= 6

    def _all_checkers_in_home(self, player):
        """Retorna True si todas las fichas del jugador (no borneadas) están en su home."""
        name = player.name
        for pt, stack in self.points.items():
            if any(c == name for c in stack):
                if not self._in_home_board(player, pt):
                    return False
        return True

    def can_move(self, player, from_point, to_point, dice_rolls):
        """
        Valida si el movimiento es legal según reglas básicas y dados.
        - Si el jugador tiene fichas en bar, únicamente puede mover desde 'bar'.
        - Bloqueo: no se puede mover a un punto con 2+ fichas enemigas.
        - Para borne off (to_point 0 or 25) exige todas en home.
        """
        if to_point is None:
            return False
        if not self._valid_point(to_point) and to_point not in (0, 25):
            return False

        name = player.name

        # si hay fichas en bar, solo reingreso desde bar
        if self.bar.get(name) and from_point != "bar":
            return False

        # mover desde tablero
        if from_point != "bar":
            if not self._valid_point(from_point) or from_point == 0 or from_point == 25:
                return False
            if not self.points[from_point] or self.points[from_point][0] != name:
                return False

            # bloqueo por 2+ fichas enemigas
            if to_point not in (0, 25) and self.points[to_point]:
                if self.points[to_point][0] != name and len(self.points[to_point]) >= 2:
                    return False

            # validar distancia con dados
            distance = abs(to_point - from_point)
            if to_point in (0, 25):
                if not self._all_checkers_in_home(player):
                    return False
                if distance not in dice_rolls:
                    return False
            else:
                if distance not in dice_rolls:
                    return False

            return True

        # reingreso desde bar
        else:
            if not self.bar.get(name):
                return False
            for d in list(dice_rolls):
                entry = self._entry_point_from_bar(player, d)
                if self.points[entry]:
                    if self.points[entry][0] != name and len(self.points[entry]) >= 2:
                        continue
                return True
            return False

    def _consume_dice_for_entry(self, player, dice_rolls, used_value):
        """Consume el valor usado de dice_rolls (maneja duplicados)."""
        if used_value in dice_rolls:
            dice_rolls.remove(used_value)
            return True
        return False

    def move_checker(self, player, from_point, to_point, dice_rolls):
        """
        Ejecuta movimiento válido:
        - Reingreso desde 'bar'
        - Golpe de ficha solitaria (hit)
        - Movimiento normal o borne off
        - Permite moverse a puntos con múltiples fichas enemigas (sin golpearlas)
        """
        name = player.name

        # reingreso desde bar
        if from_point == "bar":
            for d in list(dice_rolls):
                entry = self._entry_point_from_bar(player, d)
                if self.points[entry] and self.points[entry][0] != name and len(self.points[entry]) >= 2:
                    continue
                if self._consume_dice_for_entry(player, dice_rolls, d):
                    if self.bar[name]:
                        self.bar[name].pop()
                    # golpe
                    if self.points[entry] and self.points[entry][0] != name and len(self.points[entry]) == 1:
                        opponent = self.points[entry].pop()
                        self.bar[opponent].append(opponent)
                    self._add_checker(player, entry)
                    return True
            return False

        # movimiento normal o borne off
        if not self.can_move(player, from_point, to_point, dice_rolls):
            return False

        distance = abs(to_point - from_point)
        if distance in dice_rolls:
            dice_rolls.remove(distance)
        else:
            return False

        # borne off
        if to_point in (0, 25):
            self._remove_checker(player, from_point)
            self.borne_off[name].append(name)
            return True

        destination = self.points[to_point]

        # golpe (1 ficha enemiga)
        if destination and destination[0] != name and len(destination) == 1:
            opponent = destination.pop()
            self.bar[opponent].append(opponent)
            self._remove_checker(player, from_point)
            self._add_checker(player, to_point)
            return True

        # más de una ficha enemiga → mover sin golpear
        if destination and destination[0] != name and len(destination) > 1:
            self._remove_checker(player, from_point)
            self._add_checker(player, to_point)
            return True

        # movimiento normal
        self._remove_checker(player, from_point)
        self._add_checker(player, to_point)
        return True

    def has_any_legal_move(self, player, dice_rolls):
        """Indica si el jugador tiene al menos un movimiento legal con los dados provistos."""
        name = player.name
        if self.bar.get(name):
            for d in set(dice_rolls):
                entry = self._entry_point_from_bar(player, d)
                if not (self.points[entry] and self.points[entry][0] != name and len(self.points[entry]) >= 2):
                    return True
            return False

        for from_pt, stack in self.points.items():
            if not stack or stack[0] != name:
                continue
            for d in set(dice_rolls):
                direction = getattr(player, "direction", +1)
                to_pt = from_pt + d if direction == +1 else from_pt - d
                if to_pt <= 0 or to_pt >= 25:
                    if not self._all_checkers_in_home(player):
                        continue
                    return True
                if 1 <= to_pt <= 24:
                    if self.points[to_pt] and self.points[to_pt][0] != name and len(self.points[to_pt]) >= 2:
                        continue
                    return True
        return False

    def get_bar(self):
        return self.bar

    def get_borne_off(self):
        return self.borne_off

    def __str__(self):
        lines = [f"{i}: {self.points[i]}" for i in range(1, 25)]
        return "\n".join(lines)
