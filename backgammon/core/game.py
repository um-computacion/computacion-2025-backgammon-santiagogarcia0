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
        d1, d2 = self.dice.roll()
        if d1 == d2:
            self.available_moves = [d1] * 4
        else:
            self.available_moves = [d1, d2]
        return (d1, d2)

    def move(self, from_point, to_point):
        """
        Intenta mover ficha:
         - Si el jugador no tiene movimientos legales con los dados -> devuelve False sin consumir ni cambiar turno.
         - Si se realiza un movimiento exitoso, consume el dado usado.
         - Si tras el movimiento no quedan available_moves -> cambia de turno automáticamente.
        """
        player = self.current_player

        if not self.available_moves:
            return False

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

    def check_winner(self):
        """Devuelve el jugador ganador si ya borneó todas sus fichas, sino None."""
        for player in self.players:
            if len(self.board.borne_off.get(player.name, [])) >= 15:
                return player
        return None

    def is_finished(self):
        """Determina si el juego terminó (victoria)."""
        return self.check_winner() is not None
