"""
Módulo game
Contiene la clase Game que gestiona el flujo principal del juego.
"""

from backgammon.core.board import Board
from backgammon.core.player import Player
from backgammon.core.dice import Dice

class Game:
    """
    Representa el juego de Backgammon.
    Controla los jugadores, el tablero y el flujo de turnos.
    """

    def __init__(self, player1=None, player2=None, on_turn_change=None):
        self.board = Board()
        self.dice = Dice()
        self.players = [
            player1 if player1 else Player("Jugador 1"),
            player2 if player2 else Player("Jugador 2"),
        ]
        self.current_turn_index = 0
        self.available_moves = []
        self.on_turn_change = on_turn_change

    def start_game(self):
        """Inicializa el tablero con fichas de ambos jugadores."""
        self.board.setup_board(self.players)
        self.current_turn_index = 0
        self.available_moves = []

    def roll_dice(self):
        """Lanza los dados y configura los movimientos disponibles."""
        if self.is_finished():
            return None
        
        d1, d2 = self.dice.roll()
        if d1 == d2:
            self.available_moves = [d1] * 4
        else:
            self.available_moves = [d1, d2]
        
        if not self.board.has_any_legal_move(self.current_player, self.available_moves):
            self.next_turn()
        
        return (d1, d2)

    def move(self, from_point, to_point):
        """Intenta mover una ficha y gestiona el estado del turno."""
        if self.is_finished() or not self.available_moves:
            return False

        player = self.current_player
        
        legal_moves = self.board.get_legal_moves(player, from_point, self.available_moves)
        if to_point not in legal_moves:
            return False

        # --- Determinar el dado utilizado ---
        roll_used = None
        if from_point == "bar":
            roll_used = to_point if player.direction == 1 else 25 - to_point
        elif to_point in (0, 25): # Bear off
            distance = abs(from_point - to_point)
            if distance in self.available_moves:
                roll_used = distance
            else: # Bear off no exacto
                roll_used = max(r for r in self.available_moves if r >= distance)
        else: # Movimiento normal
            roll_used = abs(to_point - from_point)

        if roll_used is None or roll_used not in self.available_moves:
            return False

        # --- Ejecutar movimiento ---
        self.board.move_checker(player, from_point, to_point)
        self.available_moves.remove(roll_used)

        # Comprobar si el turno debe terminar
        if not self.available_moves or not self.board.has_any_legal_move(player, self.available_moves):
            self.next_turn()
        
        return True

    def next_turn(self):
        """Cambia el turno al siguiente jugador y limpia los dados."""
        self.current_turn_index = 1 - self.current_turn_index
        self.available_moves = []
        if self.on_turn_change:
            self.on_turn_change()

    @property
    def current_player(self):
        return self.players[self.current_turn_index]

    @property
    def winner(self):
        """Devuelve el ganador si ha sacado todas sus fichas."""
        for player in self.players:
            if len(self.board.borne_off.get(player.name, [])) == 15:
                return player
        return None

    def is_finished(self):
        return self.winner is not None
