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
    """Dibuja el tablero y fichas de Backgammon en Pygame."""

    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()

        # Márgenes y medidas - ajustes para que no se crucen triángulos ni borde
        self.outer_margin = 28
        self.inner_margin = 60
        self.bar_width = 40
        self.gap_between_rows = 40  # espacio entre fila superior e inferior (visual)

        # Área disponible para los 12 triángulos de cada lado
        play_width = self.width - 2 * self.inner_margin - self.bar_width
        self.triangle_width = play_width // 12
        # altura máxima para un triángulo (por fila)
        available_height = self.height - 2 * self.inner_margin - self.gap_between_rows
        self.triangle_height = available_height // 2

        # fichas (radio y separación)
        self.checker_radius = max(8, int(self.triangle_width * 0.42))
        self.checker_spacing = int(self.checker_radius * 1.6)

        # posiciones iniciales (solo para mostrar; el motor real de juego controla datos)
        # formato: point_number: count
        self.start_positions = {
            # usando convención simple de muestra (no afecta lógica de tests)
            # puedes adaptar si quieres exactos estándares
            1: 2, 12: 5, 17: 3, 19: 5,
            24: 2, 13: 5, 8: 3, 6: 5
        }

    # -------------------------------
    # Utilidades de layout
    # -------------------------------
    def _bar_x(self):
        """Coordenada X (izquierda) de la barra central."""
        return self.inner_margin + 6 * self.triangle_width

    def _column_x(self, column_index):
        """
        column_index: 0..11
        retorna x izquierdo del triángulo en esa columna (sin contar bar)
        columnas 0..5 -> izquierda, 6..11 -> derecha (después de bar)
        """
        if column_index < 6:
            return self.inner_margin + column_index * self.triangle_width
        else:
            # columnas 6..11 están a la derecha de la barra
            right_index = column_index - 6
            return self._bar_x() + self.bar_width + right_index * self.triangle_width

    def _point_to_column(self, point):
        """
        Map punto 1..24 a columna_index 0..11 y orientation (top/bottom).
        Convención usada:
          - puntos 1..12 -> fila inferior (bottom), se mapean de derecha a izquierda
          - puntos 13..24 -> fila superior (top), se mapean de left->right
        Mapeo visual clásico: en la vista, bottom right es punto 1.
        """
        if 1 <= point <= 12:
            # bottom row: map point 1 -> column 11, point 12 -> column 0
            col = 12 - point  # 11..0
            top = False
        else:
            # top row: point 13 -> column 0, point 24 -> column 11
            col = (point - 13)  # 0..11
            top = True
        # col is 0..11
        return col, top

    # -------------------------------
    # Dibujo del tablero y triángulos
    # -------------------------------
    def draw_board(self):
        # fondo general
        self.surface.fill(GREEN)

        # recuadro del área de juego (un poco más claro)
        play_left = self.inner_margin - 6
        play_top = self.inner_margin - 6
        play_w = self.width - 2 * (self.inner_margin - 6)
        play_h = self.height - 2 * (self.inner_margin - 6)
        pygame.draw.rect(self.surface, PLAY_AREA, (play_left, play_top, play_w, play_h))

        # Triángulos: top and bottom
        self._draw_triangles(top=True)
        self._draw_triangles(top=False)

        # Barra central (altura dentro del área de juego)
        bar_x = self._bar_x()
        bar_y = self.inner_margin
        bar_h = self.height - 2 * self.inner_margin
        pygame.draw.rect(self.surface, (60, 30, 10), (bar_x, bar_y, self.bar_width, bar_h))

        # Marco exterior (no se superpone con triángulos)
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

        # Dibujar fichas de ejemplo (iniciales)
        self._draw_initial_checkers()

    def _draw_triangles(self, top=True):
        """
        Dibuja 12 triángulos por fila.
        top=True -> triángulos apuntan hacia abajo (superiores)
        top=False -> triángulos apuntan hacia arriba (inferiores)
        """
        # dirección vertical del vértice del triángulo
        direction = 1 if top else -1

        # y base para la fila de triángulos (la base es la línea superior del triángulo para bottom,
        # y la línea inferior para top)
        if top:
            base_y = self.inner_margin  # triángulos superiores arrancan desde inner_margin
            # se desplazará hacia abajo para que el vértice apunte hacia abajo
            y_offset = 0
        else:
            base_y = self.height - self.inner_margin  # triángulos inferiores arrancan desde inner_margin abajo
            y_offset = 0

        for col in range(12):
            # color alternado entre triángulos
            color = LIGHT_BROWN if col % 2 == 0 else DARK_BROWN
            x_left = self._column_x(col)
            x_right = x_left + self.triangle_width

            # calcular vértice Y
            if top:
                apex_y = base_y + direction * self.triangle_height
                p1 = (x_left, base_y + y_offset)
                p2 = (x_right, base_y + y_offset)
                p3 = (x_left + self.triangle_width / 2, apex_y)
            else:
                apex_y = base_y + direction * self.triangle_height
                p1 = (x_left, base_y + y_offset)
                p2 = (x_right, base_y + y_offset)
                p3 = (x_left + self.triangle_width / 2, apex_y)

            pygame.draw.polygon(self.surface, color, [p1, p2, p3])

    # -------------------------------
    # Fichas
    # -------------------------------
    def _draw_initial_checkers(self):
        """
        Dibuja un conjunto de fichas de ejemplo basado en self.start_positions.
        Contempla apilamiento dentro del triángulo sin salirse.
        """
        for point, count in self.start_positions.items():
            for idx in range(count):
                x, y = self._checker_position_on_point(point, idx)
                # color alternado: mantengo blanco/negro como ejemplo
                color = WHITE if point % 2 == 0 else BLACK
                pygame.draw.circle(self.surface, color, (x, y), self.checker_radius)
                pygame.draw.circle(self.surface, BORDER_COLOR, (x, y), self.checker_radius, 2)

    def _checker_position_on_point(self, point, index_in_stack):
        """
        Devuelve coordenadas (x,y) para una ficha dada en 'point' (1..24) y su índice (0..).
        index_in_stack=0 => ficha más cercana al vértice (apilamiento hacia la base)
        """
        col, top = self._point_to_column(point)
        x_left = self._column_x(col)
        center_x = int(x_left + self.triangle_width / 2)

        # para top True (triángulos superiores): las fichas "empujan" desde la base (arriba)
        # colocamos la primera ficha cerca del vértice y expandimos hacia el interior
        if top:
            apex_y = self.inner_margin + self.triangle_height  # vértice inferior de los triángulos superiores
            # queremos apilar hacia abajo desde apex_y - (checker's radius) hacia base
            y = int(apex_y - self.checker_radius - index_in_stack * self.checker_spacing)
            # asegurarnos que no salga por encima de inner_margin
            min_y = self.inner_margin + self.checker_radius
            if y < min_y:
                y = min_y + index_in_stack * self.checker_spacing
        else:
            apex_y = self.height - self.inner_margin - self.triangle_height  # vértice superior de triángulos inferiores
            y = int(apex_y + self.checker_radius + index_in_stack * self.checker_spacing)
            max_y = self.height - self.inner_margin - self.checker_radius
            if y > max_y:
                y = max_y - index_in_stack * self.checker_spacing

        return center_x, y
