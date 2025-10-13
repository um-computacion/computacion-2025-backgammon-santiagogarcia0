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
        self.points = {i: [] for i in range(1, 25)}
        self.points[1] = [players[0].name] * 15
        self.points[24] = [players[1].name] * 15

        self.bar = {p.name: [] for p in players}
        self.borne_off = {p.name: [] for p in players}

        try:
            players[0].direction = +1
            players[1].direction = -1
        except Exception:
            pass

    def _valid_point(self, point):
        return 0 <= point <= 25

    def _remove_checker(self, player, from_point):
        self.points[from_point].remove(player.name)

    def _add_checker(self, player, to_point):
        self.points[to_point].append(player.name)

    def _entry_point_from_bar(self, player, dice_value):
        direction = getattr(player, "direction", +1)
        if direction == +1:
            return dice_value
        else:
            return 25 - dice_value

    def _in_home_board(self, player, point):
        direction = getattr(player, "direction", +1)
        if direction == +1:
            return 19 <= point <= 24
        else:
            return 1 <= point <= 6

    def _all_checkers_in_home(self, player):
        name = player.name
        for pt, stack in self.points.items():
            if any(c == name for c in stack):
                if not self._in_home_board(player, pt):
                    return False
        return True

    def can_move(self, player, from_point, to_point, dice_rolls):
        if to_point is None:
            return False
        if not self._valid_point(to_point) and to_point not in (0, 25):
            return False

        name = player.name

        if self.bar.get(name) and from_point != "bar":
            return False

        if from_point != "bar":
            if not self._valid_point(from_point) or from_point == 0 or from_point == 25:
                return False
            if not self.points[from_point] or self.points[from_point][0] != name:
                return False

            if to_point not in (0, 25) and self.points[to_point]:
                if self.points[to_point][0] != name and len(self.points[to_point]) >= 2:
                    return False

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
        if used_value in dice_rolls:
            dice_rolls.remove(used_value)
            return True
        return False

    def move_checker(self, player, from_point, to_point, dice_rolls):
        name = player.name

        if from_point == "bar":
            for d in list(dice_rolls):
                entry = self._entry_point_from_bar(player, d)
                if self.points[entry] and self.points[entry][0] != name and len(self.points[entry]) >= 2:
                    continue
                if self._consume_dice_for_entry(player, dice_rolls, d):
                    self.bar[name].pop()
                    if self.points[entry] and self.points[entry][0] != name and len(self.points[entry]) == 1:
                        opponent = self.points[entry].pop()
                        self.bar[opponent].append(opponent)
                    self._add_checker(player, entry)
                    return True
            return False

        if not self.can_move(player, from_point, to_point, dice_rolls):
            return False

        distance = abs(to_point - from_point)
        if distance in dice_rolls:
            dice_rolls.remove(distance)
        else:
            return False

        if to_point in (0, 25):
            self._remove_checker(player, from_point)
            self.borne_off[name].append(name)
            return True

        if self.points[to_point] and self.points[to_point][0] != name and len(self.points[to_point]) == 1:
            opponent = self.points[to_point].pop()
            self.bar[opponent].append(opponent)

        self._remove_checker(player, from_point)
        self._add_checker(player, to_point)
        return True

    def has_any_legal_move(self, player, dice_rolls):
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
