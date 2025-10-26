import pygame

# Colores
GREEN = (34, 139, 34)
PLAY_AREA = (40, 150, 80)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
BORDER_COLOR = (0, 0, 0)
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)

class BoardRenderer:
    """Dibuja el tablero y las fichas de Backgammon en Pygame."""

    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()

        # Márgenes y medidas
        self.outer_margin = 28
        self.inner_margin = 60
        self.bar_width = 40
        self.gap_between_rows = 40

        # Área disponible para los 12 triángulos de cada lado
        play_width = self.width - 2 * self.inner_margin - self.bar_width
        self.triangle_width = play_width // 12
        available_height = self.height - 2 * self.inner_margin - self.gap_between_rows
        self.triangle_height = available_height // 2

        # Fichas
        self.checker_radius = max(8, int(self.triangle_width * 0.42))
        self.checker_spacing = int(self.checker_radius * 1.6)

        # Posiciones iniciales (simplificadas)
        self.start_positions = {
            1: 2, 12: 5, 17: 3, 19: 5,
            24: 2, 13: 5, 8: 3, 6: 5
        }

    # -------------------------------
    # Utilidades de layout
    # -------------------------------
    def _bar_x(self):
        return self.inner_margin + 6 * self.triangle_width

    def _column_x(self, column_index):
        if column_index < 6:
            return self.inner_margin + column_index * self.triangle_width
        else:
            right_index = column_index - 6
            return self._bar_x() + self.bar_width + right_index * self.triangle_width

    def _point_to_column(self, point):
        if 1 <= point <= 12:
            col = 12 - point
            top = False
        else:
            col = (point - 13)
            top = True
        return col, top

    # -------------------------------
    # Dibujo del tablero
    # -------------------------------
    def draw_board(self):
        self.surface.fill(GREEN)

        # Área de juego
        play_left = self.inner_margin - 6
        play_top = self.inner_margin - 6
        play_w = self.width - 2 * (self.inner_margin - 6)
        play_h = self.height - 2 * (self.inner_margin - 6)
        pygame.draw.rect(self.surface, PLAY_AREA, (play_left, play_top, play_w, play_h))

        # Triángulos
        self._draw_triangles(top=True)
        self._draw_triangles(top=False)

        # Barra central
        bar_x = self._bar_x()
        bar_y = self.inner_margin
        bar_h = self.height - 2 * self.inner_margin
        pygame.draw.rect(self.surface, (60, 30, 10), (bar_x, bar_y, self.bar_width, bar_h))

        # Marco exterior
        pygame.draw.rect(
            self.surface,
            BORDER_COLOR,
            (self.outer_margin, self.outer_margin,
             self.width - 2 * self.outer_margin,
             self.height - 2 * self.outer_margin),
            6,
            border_radius=8,
        )

    def _draw_triangles(self, top=True):
        direction = 1 if top else -1
        base_y = self.inner_margin if top else self.height - self.inner_margin

        for col in range(12):
            color = LIGHT_BROWN if col % 2 == 0 else DARK_BROWN
            x_left = self._column_x(col)
            x_right = x_left + self.triangle_width
            apex_y = base_y + direction * self.triangle_height

            p1 = (x_left, base_y)
            p2 = (x_right, base_y)
            p3 = (x_left + self.triangle_width / 2, apex_y)

            pygame.draw.polygon(self.surface, color, [p1, p2, p3])

    # -------------------------------
    # Posiciones de fichas
    # -------------------------------
    def get_checker_positions(self):
        """Devuelve lista [(x, y, color), ...] para todas las fichas iniciales."""
        positions = []
        player_one_points = [1, 12, 17, 19]
        for point, count in self.start_positions.items():
            for idx in range(count):
                x, y = self._checker_position_on_point(point, idx)
                color = WHITE if point in player_one_points else BLACK
                positions.append((x, y, color, point))
        return positions

    def _checker_position_on_point(self, point, index_in_stack):
        col, top = self._point_to_column(point)
        x_left = self._column_x(col)
        center_x = int(x_left + self.triangle_width / 2)

        # ✅ Fichas cerca de la base (no en la punta)
        if top:
            base_y = self.inner_margin
            y = int(base_y + self.checker_radius + index_in_stack * self.checker_spacing)
        else:
            base_y = self.height - self.inner_margin
            y = int(base_y - self.checker_radius - index_in_stack * self.checker_spacing)

        return center_x, y