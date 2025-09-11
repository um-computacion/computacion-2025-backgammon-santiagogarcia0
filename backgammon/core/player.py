"""
Módulo player
Contiene la clase Player que representa a un jugador.
"""

class Player:
    """
    Representa a un jugador de Backgammon.
    """

    def __init__(self, name):
        self.__name__ = name
        self.__checkers__ = 15

    def remove_checker(self):
        """Quita una ficha del jugador si tiene alguna."""
        if self.__checkers__ > 0:
            self.__checkers__ -= 1
        else:
            raise ValueError("No se pueden quitar más fichas.")

    def add_checker(self):
        """Agrega una ficha al jugador."""
        self.__checkers__ += 1

    def has_won(self):
        """Retorna True si el jugador no tiene más fichas."""
        return self.__checkers__ == 0

    def __str__(self):
        """Representación simple del jugador."""
        return f"{self.__name__} con {self.__checkers__} fichas restantes"
