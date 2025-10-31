import pygame

class CheckerManager:
    """Maneja la interacción del jugador con las fichas (clic)."""

    def __init__(self, board_renderer, game):
        self.board_renderer = board_renderer
        self.game = game
        self.selected_point = None
        self.legal_moves = []

    def _screen_to_point(self, pos):
        """Convierte coordenadas de pantalla a un punto del tablero de forma robusta."""
        mx, my = pos
        br = self.board_renderer

        # Determinar si el clic fue en la fila superior o inferior
        if br.inner_margin < my < br.inner_margin + br.triangle_height:
            row = 'top'
        elif br.height - br.inner_margin - br.triangle_height < my < br.height - br.inner_margin:
            row = 'bottom'
        else:
            # Comprobar si el clic fue en la barra para deseleccionar
            if br.width/2 - br.bar_width/2 < mx < br.width/2 + br.bar_width/2:
                return "bar"
            return None

        # Determinar en qué columna se hizo clic
        col = -1
        # Lado izquierdo del tablero
        if br.inner_margin < mx < br.width / 2 - br.bar_width / 2:
            col = int((mx - br.inner_margin) / br.triangle_width)
        # Lado derecho del tablero
        elif br.width / 2 + br.bar_width / 2 < mx < br.width - br.inner_margin:
            col = 6 + int((mx - (br.width / 2 + br.bar_width / 2)) / br.triangle_width)

        if col == -1:
            return None

        # Mapear fila y columna a punto de backgammon
        if row == 'top':
            return 13 + col
        else: # row == 'bottom'
            return 12 - col

    def handle_event(self, event):
        """Procesa clics para seleccionar y mover fichas."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            point = self._screen_to_point(event.pos)
            
            if self.selected_point is None:
                # Intentar seleccionar una ficha
                current_player = self.game.current_player
                if point == "bar" and self.game.board.bar[current_player.name]:
                    self.selected_point = "bar"
                    self.legal_moves = self.game.board.get_legal_moves(current_player, "bar", self.game.available_moves)
                elif isinstance(point, int) and self.game.board.points[point] and self.game.board.points[point][0] == current_player.name:
                    self.selected_point = point
                    self.legal_moves = self.game.board.get_legal_moves(current_player, point, self.game.available_moves)
            else:
                # Intentar mover a un punto legal o deseleccionar
                if point in self.legal_moves:
                    self.game.move(self.selected_point, point)
                    self.selected_point = None
                    self.legal_moves = []
                elif isinstance(point, int) and self.game.board.points[point] and self.game.board.points[point][0] == self.game.current_player.name:
                    # Cambiar selección a otra ficha propia
                    self.selected_point = point
                    self.legal_moves = self.game.board.get_legal_moves(self.game.current_player, point, self.game.available_moves)
                else:
                    # Deseleccionar si se hace clic en un lugar inválido
                    self.selected_point = None
                    self.legal_moves = []
