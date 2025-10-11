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
        # Configuración temporal/necesaria si no se llama setup_board
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
        y establece dirección de movimiento para cada jugador:
            - players[0] starts at point 1 and moves toward 25 (direction = +1)
            - players[1] starts at point 24 and moves toward 0  (direction = -1)
        También inicializa bar y borne_off.
        """
        # Posiciones estándar simplificadas: colocar todas en 1 y 24 para pruebas
        self.points = {i: [] for i in range(1, 25)}
        self.points[1] = [players[0].name] * 15
        self.points[24] = [players[1].name] * 15

        # Inicializar estructuras
        self.bar = {p.name: [] for p in players}
        self.borne_off = {p.name: [] for p in players}

        # Asignar dirección y home-range en el propio objeto player para facilitar lógica
        # players[0] moves from 1 -> 24 -> borne at 25 (direction +1)
        # players[1] moves from 24 -> 1 -> borne at 0 (direction -1)
        try:
            players[0].direction = +1
            players[1].direction = -1
        except Exception:
            # si players no tiene atributos custom no falla el setup
            pass

    def _valid_point(self, point):
        """Devuelve True si el punto está dentro del rango permitido (0 y 25 incluidos para borne off)."""
        return 0 <= point <= 25

    def _remove_checker(self, player, from_point):
        """Quita una ficha de un punto (asume validez)."""
        self.points[from_point].remove(player.name)

    def _add_checker(self, player, to_point):
        """Agrega una ficha a un punto (asume validez)."""
        self.points[to_point].append(player.name)

    def _entry_point_from_bar(self, player, dice_value):
        """
        Calcula punto de entrada desde la barra según jugador y dado.
        - Si direction == +1 (player empezando en 1): entry = dice_value (1..6)
        - Si direction == -1 (player empezando en 24): entry = 25 - dice_value (24..19)
        """
        direction = getattr(player, "direction", +1)
        if direction == +1:
            return dice_value
        else:
            return 25 - dice_value

    def _in_home_board(self, player, point):
        """
        Verifica si un punto pertenece a la zona "home" del jugador (últimos 6 puntos).
        Para direction +1 (player desde 1): home = 19..24
        Para direction -1 (player desde 24): home = 1..6
        """
        direction = getattr(player, "direction", +1)
        if direction == +1:
            return 19 <= point <= 24
        else:
            return 1 <= point <= 6

    def _all_checkers_in_home(self, player):
        """
        Retorna True si todas las fichas del jugador (no borneadas) están en su home board.
        (útil para permitir borneado)
        """
        name = player.name
        # contar fichas en tablero (no borneadas, no bar)
        for pt, stack in self.points.items():
            if any(c == name for c in stack):
                if not self._in_home_board(player, pt):
                    return False
        # si no encontró fichas fuera del home, ok
        return True

    def can_move(self, player, from_point, to_point, dice_rolls):
        """
        Valida si el movimiento es legal según reglas básicas y dados.
        - Si el jugador tiene fichas en bar, únicamente puede mover desde bar.
        - Bloqueo: no se puede mover a un punto que tenga 2+ fichas enemigas.
        - Si intenta bornar (to_point == 0 or 25), se requiere que todas las fichas estén en home.
        - to_point puede calcularse desde bar: si from_point == 'bar' se valida la entrada.
        """
        # Validar índices
        if to_point is None:
            return False
        if not self._valid_point(to_point) and to_point not in (0, 25):
            return False

        name = player.name

        # Si el jugador tiene fichas en bar, sólo puede reingresar desde bar
        if self.bar.get(name) and from_point != "bar":
            return False

        # Moviendo desde tablero normal
        if from_point != "bar":
            if not self._valid_point(from_point) or from_point == 0 or from_point == 25:
                return False
            if not self.points[from_point] or self.points[from_point][0] != name:
                return False

            # Bloqueo: si destino tiene 2+ fichas enemigas → no se puede
            if to_point not in (0, 25) and self.points[to_point]:
                if self.points[to_point][0] != name and len(self.points[to_point]) >= 2:
                    return False

            # Validar distancia con dados
            distance = abs(to_point - from_point)
            if to_point in (0, 25):
                # borneado: sólo si todas en home y distance in dice (simplificado)
                if not self._all_checkers_in_home(player):
                    return False
                if distance not in dice_rolls:
                    return False
            else:
                if distance not in dice_rolls:
                    return False

            return True

        # Moviendo desde BAR
        else:
            # debe existir al menos una ficha en bar
            if not self.bar.get(name):
                return False
            # comprobar que alguno de los dados permita la entrada
            for d in list(dice_rolls):
                entry = self._entry_point_from_bar(player, d)
                # block if entry point has 2+ enemy checkers
                if self.points[entry]:
                    if self.points[entry][0] != name and len(self.points[entry]) >= 2:
                        continue  # no vale este dado, probar otro
                # si el entry es válido y no bloqueado, y está dentro del tablero, permitimos
                return True
            return False

    def _consume_dice_for_entry(self, player, dice_rolls, used_value):
        """Consume used dice value from dice_rolls (handles duplicates)."""
        if used_value in dice_rolls:
            dice_rolls.remove(used_value)
            return True
        return False

    def move_checker(self, player, from_point, to_point, dice_rolls):
        """
        Mueve ficha si el movimiento es válido con los dados disponibles.
        Soporta:
         - reingreso desde 'bar' (from_point == "bar")
         - golpe de fichas solitarias
         - borneado (si todas en home)
         - bloqueo por 2+ fichas enemigas
        """
        name = player.name

        if from_point == "bar":
            # intentar reingreso usando alguno de los dados
            for d in list(dice_rolls):
                entry = self._entry_point_from_bar(player, d)
                # si punto bloqueado por 2+ enemigas, no puede con ese d
                if self.points[entry] and self.points[entry][0] != name and len(self.points[entry]) >= 2:
                    continue
                # usar este d para entrar
                if self._consume_dice_for_entry(player, dice_rolls, d):
                    # sacar ficha del bar y poner en entry (captura si hay 1 rival)
                    self.bar[name].pop()
                    # golpe ?
                    if self.points[entry] and self.points[entry][0] != name and len(self.points[entry]) == 1:
                        opponent = self.points[entry].pop()
                        self.bar[opponent].append(opponent)
                    self._add_checker(player, entry)
                    return True
            return False

        # movimiento normal o borneado
        if not self.can_move(player, from_point, to_point, dice_rolls):
            return False

        distance = abs(to_point - from_point)
        # consumir dado
        if distance in dice_rolls:
            dice_rolls.remove(distance)
        else:
            # safety: shouldn't happen due to can_move, pero por si acaso
            return False

        # borneado
        if to_point in (0, 25):
            # ya validado all_in_home en can_move
            self._remove_checker(player, from_point)
            self.borne_off[name].append(name)
            return True

        # golpe (hit)
        if self.points[to_point] and self.points[to_point][0] != name and len(self.points[to_point]) == 1:
            opponent = self.points[to_point].pop()
            self.bar[opponent].append(opponent)

        # movimiento normal
        self._remove_checker(player, from_point)
        self._add_checker(player, to_point)
        return True

    def has_any_legal_move(self, player, dice_rolls):
        """
        Indica si el jugador tiene al menos un movimiento legal con los dados provistos.
        Usado por Game para decidir si pasar turno.
        """
        name = player.name
        # si hay fichas en bar, verificar reingreso posible
        if self.bar.get(name):
            for d in set(dice_rolls):
                entry = self._entry_point_from_bar(player, d)
                if not (self.points[entry] and self.points[entry][0] != name and len(self.points[entry]) >= 2):
                    return True
            return False

        # probar cada ficha en tablero
        for from_pt, stack in self.points.items():
            if not stack or stack[0] != name:
                continue
            for d in set(dice_rolls):
                # calcular destino según direction
                direction = getattr(player, "direction", +1)
                if direction == +1:
                    to_pt = from_pt + d
                else:
                    to_pt = from_pt - d
                # borneado objetivo posible?
                if to_pt <= 0 or to_pt >= 25:
                    # allowed only if all in home
                    if not self._all_checkers_in_home(player):
                        continue
                    return True
                # within board
                if 1 <= to_pt <= 24:
                    # blocked?
                    if self.points[to_pt] and self.points[to_pt][0] != name and len(self.points[to_pt]) >= 2:
                        continue
                    return True
        return False

    def get_bar(self):
        return self.bar

    def get_borne_off(self):
        return self.borne_off

    def __str__(self):
        """Representación simplificada del tablero."""
        lines = [f"{i}: {self.points[i]}" for i in range(1, 25)]
        return "\n".join(lines)
