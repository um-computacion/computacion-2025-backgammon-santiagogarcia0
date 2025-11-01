import pygame

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.buttons = {
            "new_game": pygame.Rect(350, 300, 300, 50),
            "exit": pygame.Rect(350, 400, 300, 50)
        }

    def draw(self):
        # Draw title
        title_text = self.title_font.render("Backgammon", True, (255, 255, 255))
        self.surface.blit(title_text, (self.surface.get_width() // 2 - title_text.get_width() // 2, 150))

        # Draw buttons
        for key, rect in self.buttons.items():
            pygame.draw.rect(self.surface, (0, 100, 0), rect)
            pygame.draw.rect(self.surface, (255, 255, 255), rect, 2)
            text = self.font.render(key.replace("_", " ").title(), True, (255, 255, 255))
            self.surface.blit(text, (rect.x + (rect.width - text.get_width()) // 2, rect.y + (rect.height - text.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    return key
        return None

class EndScreen(Menu):
    def __init__(self, surface, winner):
        super().__init__(surface)
        self.winner = winner
    
    def draw(self):
        # Draw title
        title_text = self.title_font.render(f"¡Gana {self.winner}!", True, (255, 255, 255))
        self.surface.blit(title_text, (self.surface.get_width() // 2 - title_text.get_width() // 2, 150))

        # Draw buttons
        for key, rect in self.buttons.items():
            pygame.draw.rect(self.surface, (0, 100, 0), rect)
            pygame.draw.rect(self.surface, (255, 255, 255), rect, 2)
            text = self.font.render(key.replace("_", " ").title(), True, (255, 255, 255))
            self.surface.blit(text, (rect.x + (rect.width - text.get_width()) // 2, rect.y + (rect.height - text.get_height()) // 2))
