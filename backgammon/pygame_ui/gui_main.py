import pygame
import sys
from backgammon.pygame_ui.gui_board import BoardRenderer
from backgammon.pygame_ui.gui_events import CheckerManager
from backgammon.pygame_ui.gui_menu import Menu
from backgammon.core.game import Game

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
        self.game_state = 'MENU'  # MENU, PLAYING, GAME_OVER

        self.game = Game()
        self.board_renderer = BoardRenderer(self.screen)
        self.checker_manager = CheckerManager(self.board_renderer, self.game)
        self.menu = Menu(self.screen)
        self.restart_button = pygame.Rect(30, 15, 150, 40)

    def restart_game(self):
        self.game.start_game()
        self.game.roll_dice()

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
                self.checker_manager.handle_event(event)
                if self.game.is_finished():
                    self.game_state = 'GAME_OVER'
            elif self.game_state == 'GAME_OVER':
                if event.type == pygame.KEYDOWN:
                    self.game_state = 'MENU'

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

            turn_text_str = f"Turn: {self.game.current_player.name}"
            turn_text = font.render(turn_text_str, True, (255, 255, 255))
            self.screen.blit(turn_text, (WINDOW_WIDTH - turn_text.get_width() - 30, 15))

            # Draw borne off checkers
            borne_off_p1 = len(self.game.board.borne_off.get(self.game.players[0].name, []))
            borne_off_p2 = len(self.game.board.borne_off.get(self.game.players[1].name, []))
            borne_off_text_p1 = font.render(f"Borne Off P1: {borne_off_p1}", True, (255, 255, 255))
            borne_off_text_p2 = font.render(f"Borne Off P2: {borne_off_p2}", True, (255, 255, 255))
            self.screen.blit(borne_off_text_p1, (30, WINDOW_HEIGHT - 60))
            self.screen.blit(borne_off_text_p2, (WINDOW_WIDTH - borne_off_text_p2.get_width() - 30, WINDOW_HEIGHT - 60))

            # Draw restart button
            pygame.draw.rect(self.screen, (0, 100, 0), self.restart_button)
            pygame.draw.rect(self.screen, (255, 255, 255), self.restart_button, 2)
            restart_text = font.render("Restart", True, (255, 255, 255))
            self.screen.blit(restart_text, (self.restart_button.x + (self.restart_button.width - restart_text.get_width()) // 2, self.restart_button.y + (self.restart_button.height - restart_text.get_height()) // 2))

        elif self.game_state == 'GAME_OVER':
            font = pygame.font.SysFont("Arial", 60, bold=True)
            winner_text = f"Winner: {self.game.winner.name}"
            text = font.render(winner_text, True, (255, 255, 255))
            self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
            
            font_small = pygame.font.SysFont("Arial", 30)
            prompt_text = font_small.render("Press any key to return to menu", True, (200, 200, 200))
            self.screen.blit(prompt_text, (WINDOW_WIDTH // 2 - prompt_text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))

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