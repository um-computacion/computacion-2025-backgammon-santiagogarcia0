class Board:
    
    """Representa el tablero de Backgammon y la posición de las fichas."""

    def __init__(self):
        # 24 puntos del tablero (cada posición empieza vacía)
        self.positions = [0] * 24
