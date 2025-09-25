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
            player2 if player2 else Player("Jugador 2")
        ]
        self.current_turn_index = 0
        self.available_moves = []

    def start_game(self):
        """Inicializa el tablero con fichas de ambos jugadores."""
        self.board.setup_board(self.players)

    def roll_dice(self):
        """Lanza los dados y configura movimientos disponibles."""
        roll = self.dice.roll()
        self.available_moves = list(roll) if roll[0] != roll[1] else [roll[0]] * 4
        return roll

    def move(self, from_point, to_point):
        """Intenta mover ficha y consume la tirada usada."""
        player = self.current_player
        success = self.board.move_checker(player, from_point, to_point, self.available_moves)
        if success:
            winner = self.check_winner()
            if winner:
                print(f"🏆 {winner.name} ha ganado la partida!")
                exit()
            if not self.available_moves:
                self.next_turn()
        return success

    def next_turn(self):
        """Cambia el turno al siguiente jugador."""
        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)
        self.available_moves = []

    @property
    def current_player(self):
        """Devuelve el jugador que tiene el turno actual."""
        return self.players[self.current_turn_index]

    def check_winner(self):
        """Devuelve el jugador ganador si ya borneó todas sus fichas."""
        for player in self.players:
            if len(self.board.borne_off[player.name]) == 15:
                return player
        return None

    def is_finished(self):
        """Determina si el juego terminó (un jugador se quedó sin fichas)."""
        return self.check_winner() is not None
