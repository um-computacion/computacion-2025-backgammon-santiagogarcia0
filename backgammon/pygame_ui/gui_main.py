import pygame
import sys
from backgammon.core.game import Game
from backgammon.pygame_ui.gui_board import BoardRenderer
from backgammon.pygame_ui.gui_events import CheckerManager
from backgammon.pygame_ui.gui_menu import Menu, EndScreen

# Configuración
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

class PygameBackgammon:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Backgammon")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = Game(on_turn_change=self.clear_dice)
        self.board_renderer = BoardRenderer(self.screen)
        self.checker_manager = CheckerManager(self.board_renderer, self.game)
        self.menu = Menu(self.screen)
        self.end_screen = None
        self.game_state = 'MENU'
        self.dice_rolls = None

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def restart_game(self):
        """Inicia o reinicia el juego."""
        self.game.start_game()
        self.dice_rolls = self.game.roll_dice()
        self.game_state = 'PLAYING'
    
    def clear_dice(self):
        """Limpia los dados de la pantalla."""
        self.dice_rolls = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.game_state == 'MENU':
                action = self.menu.handle_event(event)
                if action == 'new_game':
                    self.restart_game()
                elif action == 'exit':
                    pygame.quit()
                    sys.exit()
            elif self.game_state == 'PLAYING':
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.game.available_moves:
                    self.dice_rolls = self.game.roll_dice()
                self.checker_manager.handle_event(event)
                if self.game.is_finished():
                    self.end_screen = EndScreen(self.screen, self.game.winner.name)
                    self.game_state = 'GAME_OVER'
            elif self.game_state == 'GAME_OVER':
                action = self.end_screen.handle_event(event)
                if action == 'new_game':
                    self.restart_game()
                elif action == 'exit':
                    pygame.quit()
                    sys.exit()
    
    def draw(self):
        if self.game_state == 'MENU':
            self.menu.draw()
        elif self.game_state == 'GAME_OVER':
            self.end_screen.draw()
        else:
            self.board_renderer.draw_board()
            self.board_renderer.draw_checkers(self.game)
            self.board_renderer.draw_bar_checkers(self.game)
            
            if self.checker_manager.selected_point is not None:
                self.board_renderer.draw_legal_moves(self.checker_manager.legal_moves)

            self.draw_game_info()

    def draw_game_info(self):
        font = pygame.font.SysFont("Arial", 28, bold=True)
        
        # Turno
        turn_text = font.render(f"Turno: {self.game.current_player.name}", True, (255, 255, 255))
        self.screen.blit(turn_text, (20, 15))

        # Dados
        if self.dice_rolls:
            dice_text = f"Dados: {self.dice_rolls}"
        elif self.game.available_moves:
            dice_text = f"Dados: {self.game.available_moves}"
        else:
            dice_text = "Tira los dados!"
            
        dice_surf = font.render(dice_text, True, (255, 255, 255))
        self.screen.blit(dice_surf, (self.screen.get_width() / 2 - dice_surf.get_width() / 2, 15))

if __name__ == "__main__":
    PygameBackgammon().run()