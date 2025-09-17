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
        self.last_roll = (0, 0)

    def roll(self):
        """Lanza los dos dados y guarda sus valores."""
        self.last_roll = (random.randint(1, 6), random.randint(1, 6))
        return self.last_roll

    def roll_double(self):
        """Lanza dos dados iguales para movimientos especiales."""
        self.last_roll = (random.randint(1, 6), random.randint(1, 6))
        return self.last_roll

    def get_values(self):
        """Devuelve la última tirada."""
        return self.last_roll
