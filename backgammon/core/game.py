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

    def __init__(self, player1=None, player2=None):
        self.board = Board()
        self.dice = Dice()
        self.players = [
            player1 if player1 else Player("Jugador 1"),
            player2 if player2 else Player("Jugador 2"),
        ]
        self.current_turn_index = 0
        self.available_moves = []

    def start_game(self):
        """Inicializa el tablero con fichas de ambos jugadores."""
        self.board.setup_board(self.players)

    def roll_dice(self):
        """Lanza los dados y configura movimientos disponibles."""
        if self.is_finished():
            return None
        d1, d2 = self.dice.roll()
        self.available_moves = [d1]*4 if d1 == d2 else [d1, d2]
        return (d1, d2)

    def move(self, from_point, to_point):
        """
        Intenta mover ficha:
        - Si el juego terminó → False
        - Si no hay dados lanzados → False
        - Si no hay movimientos legales → pasar turno y False
        - Si movimiento válido → actualiza dados
        - Si no quedan dados → cambia turno
        """
        if self.is_finished():
            return False
        if not self.available_moves:
            return False

        player = self.current_player

        if not self.board.has_any_legal_move(player, list(self.available_moves)):
            self.next_turn()
            return False

        moved = self.board.move_checker(player, from_point, to_point, self.available_moves)

        if moved and not self.available_moves:
            self.next_turn()

        return moved

    def next_turn(self):
        """Cambia el turno al siguiente jugador y limpia las tiradas pendientes."""
        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)
        self.available_moves = []

    @property
    def current_player(self):
        """Devuelve el jugador en turno."""
        return self.players[self.current_turn_index]

    @property
    def winner(self):
        """Devuelve el jugador ganador si ya borneó todas sus fichas, sino None."""
        for player in self.players:
            if len(self.board.borne_off.get(player.name, [])) >= 15:
                return player
        return None

    def check_winner(self):
        """Alias por compatibilidad."""
        return self.winner

    def is_finished(self):
        """Determina si el juego terminó."""
        return self.winner is not None
