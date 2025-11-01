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
        self.bar = {}
        self.borne_off = {}

    def setup_board(self, players):
        """Configura el tablero inicial con las fichas de los jugadores."""
        self.points = {i: [] for i in range(1, 25)}
        
        p1_name = players[0].name
        p2_name = players[1].name

        self.points[24] = [p1_name] * 2
        self.points[13] = [p1_name] * 5
        self.points[8] = [p1_name] * 3
        self.points[6] = [p1_name] * 5

        self.points[1] = [p2_name] * 2
        self.points[12] = [p2_name] * 5
        self.points[17] = [p2_name] * 3
        self.points[19] = [p2_name] * 5

        self.bar = {p.name: [] for p in players}
        self.borne_off = {p.name: [] for p in players}

        players[0].direction = -1
        players[1].direction = 1

    def _valid_point(self, point):
        return 0 <= point <= 25

    def _remove_checker(self, player_name, from_point):
        if from_point == "bar":
            self.bar[player_name].pop()
        else:
            self.points[from_point].pop()

    def _add_checker(self, player_name, to_point):
        self.points[to_point].append(player_name)

    def _entry_point_from_bar(self, player, dice_value):
        return dice_value if player.direction == 1 else 25 - dice_value

    def _all_checkers_in_home(self, player):
        """Verifica si todas las fichas de un jugador están en su home board."""
        home_range = range(19, 25) if player.direction == 1 else range(1, 7)
        for i in range(1, 25):
            if i not in home_range and self.points[i] and self.points[i][0] == player.name:
                return False
        return True

    def get_legal_moves(self, player, from_point, dice_rolls):
        """Calcula los movimientos legales desde un punto dado."""
        if from_point == "bar":
            legal_moves = []
            for roll in dice_rolls:
                entry_point = self._entry_point_from_bar(player, roll)
                target = self.points[entry_point]
                if len(target) <= 1 or target[0] == player.name:
                    legal_moves.append(entry_point)
            return list(set(legal_moves))

        legal_moves = []
        direction = player.direction
        can_bear_off = self._all_checkers_in_home(player) and not self.bar[player.name]

        for roll in dice_rolls:
            to_point = from_point + roll * direction
            
            # Movimiento de salida (bear off)
            if can_bear_off:
                if (direction == 1 and to_point == 25) or (direction == -1 and to_point == 0):
                    legal_moves.append(to_point)
                    continue
                
                # Regla del número mayor
                if (direction == 1 and to_point > 25) or (direction == -1 and to_point < 1):
                    is_highest_checker = True
                    home_board_points = range(19, 25) if player.direction == 1 else range(1, 7)
                    for p in home_board_points:
                        if p > from_point and self.points[p] and self.points[p][0] == player.name:
                            is_highest_checker = False
                            break
                    if is_highest_checker:
                        legal_moves.append(25 if direction == 1 else 0)

            # Movimiento normal
            if 1 <= to_point <= 24:
                target_point = self.points[to_point]
                is_blocked = len(target_point) > 1 and target_point[0] != player.name
                if not is_blocked:
                    legal_moves.append(to_point)
                    
        return legal_moves
    
    def has_any_legal_move(self, player, dice_rolls):
        """Verifica si el jugador tiene algún movimiento legal."""
        if self.bar[player.name]:
            return any(self.get_legal_moves(player, "bar", dice_rolls))
        
        for p in range(1, 25):
            if self.points[p] and self.points[p][0] == player.name:
                if any(self.get_legal_moves(player, p, dice_rolls)):
                    return True
        return False

    def move_checker(self, player, from_point, to_point):
        """Mueve una ficha en el tablero, asumiendo que el movimiento es legal."""
        player_name = player.name
        
        self._remove_checker(player_name, from_point)

        # Si es bear off
        if to_point in (0, 25):
            self.borne_off[player_name].append(player_name)
            return True

        # Si hay una ficha enemiga (hit)
        if self.points[to_point] and self.points[to_point][0] != player_name:
            opponent_name = self.points[to_point].pop()
            self.bar[opponent_name].append(opponent_name)
        
        self._add_checker(player_name, to_point)
        return True