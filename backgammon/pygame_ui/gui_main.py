import pygame
import sys
from pygame_ui.gui_board import BoardRenderer
from pygame_ui.gui_events import CheckerManager

# ============================
# Configuración inicial
# ============================

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60
BACKGROUND_COLOR = (30, 120, 70)

# ============================
# Clase principal del juego
# ============================

class PygameBackgammon:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Backgammon - Pygame UI")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.board_renderer = BoardRenderer(self.screen)
        self.checker_manager = CheckerManager(self.board_renderer)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            else:
                self.checker_manager.handle_event(event)

    def draw_board(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.board_renderer.draw_board()
        self.checker_manager.draw(self.screen)

        font = pygame.font.SysFont("Arial", 32, bold=True)
        text = font.render("Backgammon (Vista Gráfica - Pygame)", True, (255, 255, 255))
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 15))

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

# ============================
# Punto de entrada
# ============================

if __name__ == "__main__":
    app = PygameBackgammon()
    app.run()