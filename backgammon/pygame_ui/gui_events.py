import pygame
from pygame_ui.gui_board import BORDER_COLOR

class CheckerManager:
    """Maneja la interacción del jugador con las fichas (clic, arrastre, suelta)."""

    def __init__(self, board_renderer):
        self.board_renderer = board_renderer
        self.checkers = []  # [(x, y, color, point)]
        self.dragging = False
        self.dragged_checker = None
        self.offset_x = 0
        self.offset_y = 0
        self.load_initial_checkers()

    def load_initial_checkers(self):
        """Carga las posiciones iniciales desde el tablero."""
        self.checkers = self.board_renderer.get_checker_positions()

    def handle_event(self, event):
        """Procesa clic, arrastre y suelta de fichas."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i, (x, y, color, point) in enumerate(reversed(self.checkers)):
                if (mx - x) ** 2 + (my - y) ** 2 <= self.board_renderer.checker_radius ** 2:
                    self.dragging = True
                    self.dragged_checker = len(self.checkers) - 1 - i
                    self.offset_x = mx - x
                    self.offset_y = my - y
                    break

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            idx = self.dragged_checker
            x, y, color, point = self.checkers[idx]
            self.checkers[idx] = (mx - self.offset_x, my - self.offset_y, color, point)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            self.dragged_checker = None

    def draw(self, surface):
        """Dibuja todas las fichas en sus posiciones actuales."""
        for (x, y, color, _) in self.checkers:
            pygame.draw.circle(surface, color, (int(x), int(y)), self.board_renderer.checker_radius)
            pygame.draw.circle(surface, BORDER_COLOR, (int(x), int(y)), self.board_renderer.checker_radius, 2)