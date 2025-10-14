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
        """Lanza los dos dados (1-6) y guarda sus valores."""
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self.last_roll = (d1, d2)
        return self.last_roll

    def roll_double(self):
        """
        Fuerza un doble para pruebas o reglas especiales.
        Siempre devuelve (x, x) y lo guarda en last_roll.
        """
        value = random.randint(1, 6)
        self.last_roll = (value, value)
        return self.last_roll

    def get_values(self):
        """Devuelve la última tirada."""
        return self.last_roll
