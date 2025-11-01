import pygame

# Colores
GREEN = (34, 139, 34)
PLAY_AREA = (40, 150, 80)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
BORDER_COLOR = (0, 0, 0)
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
HIGHLIGHT_COLOR = (0, 255, 0, 100)  # Verde semitransparente para resaltar

class BoardRenderer:
    """Dibuja el tablero y las fichas de Backgammon en Pygame."""

    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()

        # Medidas
        self.inner_margin = 60
        self.bar_width = 80  # Barra más ancha
        self.gap_between_rows = 40  # Espacio entre triángulos
        
        play_width = self.width - 2 * self.inner_margin - self.bar_width
        self.triangle_width = play_width // 12
        self.triangle_height = (self.height - 2 * self.inner_margin - self.gap_between_rows) // 2
        self.checker_radius = int(self.triangle_width * 0.42)

    def draw_board(self):
        """Dibuja el tablero de juego."""
        self.surface.fill(GREEN)
        pygame.draw.rect(self.surface, PLAY_AREA, (self.inner_margin, self.inner_margin, self.width - 2 * self.inner_margin, self.height - 2 * self.inner_margin))
        
        # Barra central
        bar_x = self.width / 2 - self.bar_width / 2
        pygame.draw.rect(self.surface, DARK_BROWN, (bar_x, self.inner_margin, self.bar_width, self.height - 2 * self.inner_margin))

        # Triángulos
        for i in range(12):
            # Invertir el color para los triángulos superiores
            color_top = DARK_BROWN if i % 2 == 0 else LIGHT_BROWN
            color_bottom = LIGHT_BROWN if i % 2 == 0 else DARK_BROWN
            
            # Calcular la posición x teniendo en cuenta la barra
            x_base = self.inner_margin + i * self.triangle_width
            if i >= 6:
                x_base += self.bar_width
            
            # Triángulos superiores (apuntan hacia abajo)
            p1_top = (x_base, self.inner_margin)
            p2_top = (x_base + self.triangle_width, self.inner_margin)
            p3_top = (x_base + self.triangle_width / 2, self.inner_margin + self.triangle_height)
            pygame.draw.polygon(self.surface, color_top, [p1_top, p2_top, p3_top])
            
            # Triángulos inferiores (apuntan hacia arriba)
            y_base_bottom = self.height - self.inner_margin
            p1_bottom = (x_base, y_base_bottom)
            p2_bottom = (x_base + self.triangle_width, y_base_bottom)
            p3_bottom = (x_base + self.triangle_width / 2, y_base_bottom - self.triangle_height)
            pygame.draw.polygon(self.surface, color_bottom, [p1_bottom, p2_bottom, p3_bottom])

    def _get_checker_pos(self, point, stack_index):
        """Calcula la posición (x, y) de una ficha en un punto."""
        col = (12 - point) if 1 <= point <= 12 else (point - 13)
        x = self.inner_margin + col * self.triangle_width + self.triangle_width / 2
        if col >= 6:
            x += self.bar_width

        if 1 <= point <= 12:  # Fila inferior
            y = self.height - self.inner_margin - self.checker_radius - stack_index * (self.checker_radius * 2)
        else:  # Fila superior
            y = self.inner_margin + self.checker_radius + stack_index * (self.checker_radius * 2)
        
        return int(x), int(y)

    def draw_checkers(self, game):
        """Dibuja las fichas en el tablero."""
        p1_name = game.players[0].name
        for point, checkers in game.board.points.items():
            for i, player_name in enumerate(checkers):
                x, y = self._get_checker_pos(point, i)
                color = WHITE if player_name == p1_name else BLACK
                pygame.draw.circle(self.surface, color, (x, y), self.checker_radius)
                pygame.draw.circle(self.surface, BORDER_COLOR, (x, y), self.checker_radius, 2)

    def draw_bar_checkers(self, game):
        """Dibuja las fichas capturadas en la barra."""
        bar_x = self.width / 2
        p1_name = game.players[0].name
        
        for i, player_name in enumerate(game.board.bar.get(p1_name, [])):
            y = self.height / 2 - self.checker_radius * 3 - i * (self.checker_radius * 2)
            pygame.draw.circle(self.surface, WHITE, (int(bar_x), int(y)), self.checker_radius)
            pygame.draw.circle(self.surface, BORDER_COLOR, (int(bar_x), int(y)), self.checker_radius, 2)
        
        p2_name = game.players[1].name
        for i, player_name in enumerate(game.board.bar.get(p2_name, [])):
            y = self.height / 2 + self.checker_radius * 3 + i * (self.checker_radius * 2)
            pygame.draw.circle(self.surface, BLACK, (int(bar_x), int(y)), self.checker_radius)
            pygame.draw.circle(self.surface, BORDER_COLOR, (int(bar_x), int(y)), self.checker_radius, 2)

    def draw_legal_moves(self, moves):
        """Resalta los movimientos legales."""
        for point in moves:
            if point in [0, 25]: # Bear off
                rect = self.get_bear_off_rect(point)
                s = pygame.Surface(rect.size, pygame.SRCALPHA)
                s.fill(HIGHLIGHT_COLOR)
                self.surface.blit(s, rect.topleft)
            else:
                x, y = self._get_checker_pos(point, 0) # Posición base
                s = pygame.Surface((self.checker_radius * 2, self.checker_radius * 2), pygame.SRCALPHA)
                s.fill(HIGHLIGHT_COLOR)
                self.surface.blit(s, (x - self.checker_radius, y - self.checker_radius))

    def get_point_rect(self, point):
        """Devuelve un rect para un punto del tablero."""
        x, y = self._get_checker_pos(point, 0)
        return pygame.Rect(x - self.checker_radius, y - self.checker_radius, self.checker_radius * 2, self.checker_radius * 2)

    def get_bear_off_rect(self, point):
        """Devuelve un rect para la zona de bear off."""
        if point == 0: # Player 1 (Negro)
            return pygame.Rect(self.width - self.inner_margin, self.height / 2, self.inner_margin, self.height / 2 - self.inner_margin)
        else: # Player 2 (Blanco)
            return pygame.Rect(self.width - self.inner_margin, self.inner_margin, self.inner_margin, self.height / 2 - self.inner_margin)
