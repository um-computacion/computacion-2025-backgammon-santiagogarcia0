"""
Módulo player
Contiene la clase Player que representa a un jugador.
"""

class Player:
    """
    Representa a un jugador de Backgammon.
    """

    def __init__(self, name, checkers=15):
        self.name = name
        self.checkers = checkers

    def remove_checker(self):
        """Quita una ficha del jugador si tiene alguna."""
        if self.checkers > 0:
            self.checkers -= 1
        else:
            raise ValueError("No se pueden quitar más fichas.")

    def add_checker(self):
        """Agrega una ficha al jugador."""
        self.checkers += 1

    def has_won(self):
        """Retorna True si el jugador no tiene más fichas."""
        return self.checkers == 0

    def move_checker(self):
        """Quita una ficha simulando un movimiento del jugador."""
        self.remove_checker()

    def __str__(self):
        return f"{self.name} con {self.checkers} fichas restantes"
