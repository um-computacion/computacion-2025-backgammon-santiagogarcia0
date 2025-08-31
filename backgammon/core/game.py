class Game:
    
    """Clase principal que gestiona el flujo del juego de Backgammon."""

    def __init__(self, players, board, dice):

        self.players = players
        self.board = board
        self.dice = dice

