import pygame
import sys
from pygame_ui.gui_board import BoardRenderer
from pygame_ui.gui_events import CheckerManager
from pygame_ui.gui_menu import Menu

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
        self.game_state = 'MENU'  # MENU, PLAYING
        self.current_turn = 'WHITE'

        self.board_renderer = BoardRenderer(self.screen)
        self.checker_manager = CheckerManager(self.board_renderer)
        self.menu = Menu(self.screen)
        self.restart_button = pygame.Rect(30, 15, 150, 40)

    def restart_game(self):
        self.checker_manager.load_initial_checkers()
        self.current_turn = 'WHITE'

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game_state = 'MENU'

            if self.game_state == 'MENU':
                action = self.menu.handle_event(event)
                if action == 'new_game':
                    self.restart_game()
                    self.game_state = 'PLAYING'
                elif action == 'exit':
                    self.running = False
            elif self.game_state == 'PLAYING':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.restart_button.collidepoint(event.pos):
                        self.restart_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    self.current_turn = 'BLACK' if self.current_turn == 'WHITE' else 'WHITE'
                self.checker_manager.handle_event(event)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        if self.game_state == 'MENU':
            self.menu.draw()
        elif self.game_state == 'PLAYING':
            self.board_renderer.draw_board()
            self.checker_manager.draw(self.screen)

            font = pygame.font.SysFont("Arial", 32, bold=True)
            text = font.render("Backgammon", True, (255, 255, 255))
            self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 15))

            turn_text = font.render(f"Turn: {self.current_turn}", True, (255, 255, 255))
            self.screen.blit(turn_text, (WINDOW_WIDTH - turn_text.get_width() - 30, 15))

            # Draw restart button
            pygame.draw.rect(self.screen, (0, 100, 0), self.restart_button)
            pygame.draw.rect(self.screen, (255, 255, 255), self.restart_button, 2)
            restart_text = font.render("Restart", True, (255, 255, 255))
            self.screen.blit(restart_text, (self.restart_button.x + (self.restart_button.width - restart_text.get_width()) // 2, self.restart_button.y + (self.restart_button.height - restart_text.get_height()) // 2))

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
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