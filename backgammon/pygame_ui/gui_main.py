import pygame
import sys

# ============================
# Configuración inicial
# ============================

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60
BACKGROUND_COLOR = (30, 120, 70)  # Verde tipo paño

# ============================
# Clase principal del juego
# ============================

class PygameBackgammon:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Backgammon - Pygame UI")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # Estado inicial
        self.running = True

    def handle_events(self):
        """Procesa eventos del usuario (clics, cerrar ventana, etc.)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw_board_base(self):
        """Dibuja un tablero simple (placeholder)."""
        self.screen.fill(BACKGROUND_COLOR)

        # Dibujar marco
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 50, 900, 600), 5)

        # Separador central (barra)
        pygame.draw.rect(self.screen, (0, 0, 0), (495, 50, 10, 600))

        # Texto temporal
        font = pygame.font.SysFont("Arial", 32)
        text = font.render("Backgammon (Vista base)", True, (255, 255, 255))
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 10))

    def run(self):
        """Bucle principal de la aplicación."""
        while self.running:
            self.handle_events()
            self.draw_board_base()
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
