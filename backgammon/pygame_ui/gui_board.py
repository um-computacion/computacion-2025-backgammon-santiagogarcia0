import pygame

GREEN = (34, 139, 34)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
BORDER_COLOR = (0, 0, 0)
BOARD_GREEN = (40, 150, 80)


class BoardRenderer:
    """Dibuja el tablero de Backgammon en Pygame."""

    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()

        # Márgenes ajustados
        self.outer_margin = 40
        self.inner_margin = 90
        self.bar_width = 40
        self.gap_between_rows = 90

        # Altura disponible para los triángulos
        total_play_height = self.height - 2 * self.inner_margin - self.gap_between_rows
        self.triangle_height = total_play_height // 2
        self.triangle_width = (self.width - 2 * self.inner_margin - self.bar_width) // 12

    def draw_board(self):
        """Dibuja tablero completo."""
        self.surface.fill(GREEN)

        # -------------------------------
        # Fondo del área de juego
        # -------------------------------
        board_x = self.outer_margin + 10
        board_y = self.outer_margin + 10
        board_w = self.width - 2 * (self.outer_margin + 10)
        board_h = self.height - 2 * (self.outer_margin + 10)

        pygame.draw.rect(self.surface, BOARD_GREEN, (board_x, board_y, board_w, board_h))

        # -------------------------------
        # Triángulos
        # -------------------------------
        self._draw_triangles(top=False)
        self._draw_triangles(top=True)

        # -------------------------------
        # Barra central (alineada con tablero interno)
        # -------------------------------
        bar_x = self.width // 2 - self.bar_width // 2
        bar_y = board_y  # Empieza en el borde interno
        pygame.draw.rect(
            self.surface,
            (60, 30, 10),
            (bar_x, bar_y, self.bar_width, board_h),
        )

        # -------------------------------
        # Marco externo
        # -------------------------------
        pygame.draw.rect(
            self.surface,
            BORDER_COLOR,
            (
                self.outer_margin,
                self.outer_margin,
                self.width - 2 * self.outer_margin,
                self.height - 2 * self.outer_margin,
            ),
            6,
            border_radius=8,
        )

    def _draw_triangles(self, top=True):
        """Dibuja los triángulos (6 por lado de la barra)."""
        if top:
            y_base = self.inner_margin
            direction = 1
            color_offset = 1
        else:
            y_base = self.height - self.inner_margin
            direction = -1
            color_offset = 0

        for side in range(2):
            for i in range(6):
                color = LIGHT_BROWN if (i + side * 6 + color_offset) % 2 == 0 else DARK_BROWN

                if side == 0:
                    x = self.inner_margin + i * self.triangle_width
                else:
                    x = (
                        self.inner_margin
                        + 6 * self.triangle_width
                        + self.bar_width
                        + i * self.triangle_width
                    )

                y_shift = self.gap_between_rows // 2 * (-1 if top else 1)

                points = [
                    (x, y_base + y_shift),
                    (x + self.triangle_width, y_base + y_shift),
                    (
                        x + self.triangle_width / 2,
                        y_base + y_shift + direction * self.triangle_height,
                    ),
                ]
                pygame.draw.polygon(self.surface, color, points)
