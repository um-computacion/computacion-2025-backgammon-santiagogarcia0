import pygame
from backgammon.pygame_ui.gui_board import BORDER_COLOR, WHITE, BLACK

class CheckerManager:
    """Maneja la interacción del jugador con las fichas (clic, arrastre, suelta)."""

    def __init__(self, board_renderer, game):
        self.board_renderer = board_renderer
        self.game = game
        self.dragging = False
        self.dragged_checker_info = None  # {'point': int, 'pos': (x, y), 'color': (r,g,b)}
        self.offset_x = 0
        self.offset_y = 0

    def _screen_to_point(self, pos):
        """Convierte coordenadas de pantalla a un punto del tablero."""
        mx, my = pos
        br = self.board_renderer

        top_row = my < br.height / 2

        col = -1
        if br.inner_margin <= mx < br._bar_x():
            col = (mx - br.inner_margin) // br.triangle_width
        elif br._bar_x() + br.bar_width <= mx < br.width - br.inner_margin:
            col = ((mx - (br._bar_x() + br.bar_width)) // br.triangle_width) + 6

        if col == -1:
            return None

        if top_row:
            point = 13 + col
        else:
            point = 12 - col
            
        return point

    def handle_event(self, event):
        """Procesa clic, arrastre y suelta de fichas."""
        br = self.board_renderer
        current_player = self.game.current_player

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.dragging:
            mx, my = event.pos
            for point_num, checkers in self.game.board.points.items():
                if checkers and checkers[0] == current_player:
                    stack_idx = len(checkers) - 1
                    cx, cy = br._checker_position_on_point(point_num, stack_idx)
                    
                    if (mx - cx) ** 2 + (my - cy) ** 2 <= br.checker_radius ** 2:
                        self.dragging = True
                        color = WHITE if current_player.name == "Jugador 1" else BLACK
                        self.dragged_checker_info = {
                            'point': point_num,
                            'pos': (cx, cy),
                            'color': color
                        }
                        self.offset_x = mx - cx
                        self.offset_y = my - cy
                        self.game.board.points[point_num].pop()
                        return

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            self.dragged_checker_info['pos'] = (mx - self.offset_x, my - self.offset_y)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            from_point = self.dragged_checker_info['point']
            to_point = self._screen_to_point(event.pos)

            moved = False
            if to_point is not None:
                moved = self.game.move(from_point, to_point)

            if not moved:
                self.game.board.points[from_point].append(current_player)

            self.dragging = False
            self.dragged_checker_info = None

    def draw(self, surface):
        """Dibuja todas las fichas basándose en el estado del juego."""
        br = self.board_renderer
        player_colors = {
            self.game.players[0].name: WHITE,
            self.game.players[1].name: BLACK
        }

        for point_num, checkers in self.game.board.points.items():
            if checkers:
                player = checkers[0]
                color = player_colors.get(player.name)
                for i in range(len(checkers)):
                    x, y = br._checker_position_on_point(point_num, i)
                    pygame.draw.circle(surface, color, (int(x), int(y)), br.checker_radius)
                    pygame.draw.circle(surface, BORDER_COLOR, (int(x), int(y)), br.checker_radius, 2)
        
        if self.dragging and self.dragged_checker_info:
            info = self.dragged_checker_info
            x, y = info['pos']
            color = info['color']
            pygame.draw.circle(surface, color, (int(x), int(y)), br.checker_radius)
            pygame.draw.circle(surface, BORDER_COLOR, (int(x), int(y)), br.checker_radius, 2)
