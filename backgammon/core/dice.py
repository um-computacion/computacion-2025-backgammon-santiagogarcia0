"""
Módulo dice
Contiene la clase Dice que representa los dados.
"""

import random

class Dice:
    """
    Representa un par de dados de Backgammon.
    """

    def __init__(self):
        self.__values__ = (0, 0)

    def roll(self):
        """Lanza los dos dados y guarda sus valores."""
        self.__values__ = (random.randint(1, 6), random.randint(1, 6))
        return self.__values__

    def get_values(self):
        """Devuelve la última tirada."""
        return self.__values__
