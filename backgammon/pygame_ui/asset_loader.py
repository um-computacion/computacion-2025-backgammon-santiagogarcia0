import pygame
import os

def load_image(filename, size=None):
    """Carga una imagen, opcionalmente la reescala."""
    # Obtener la ruta absoluta al directorio de este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construir la ruta al directorio de assets (asumiendo que está dos niveles arriba)
    assets_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'assets'))
    path = os.path.join(assets_dir, 'images', filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except (pygame.error, FileNotFoundError):
        print(f"Advertencia: No se pudo cargar la imagen '{path}'. Se usará un color sólido.")
        surface = pygame.Surface(size if size else (50, 50))
        surface.fill((128, 0, 128))  # Un color distintivo para notar que falta el asset
        return surface

def load_sound(filename):
    """Carga un efecto de sonido, o un objeto 'dummy' si no se encuentra."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'assets'))
    path = os.path.join(assets_dir, 'sounds', filename)
    if not os.path.exists(path):
        print(f"Advertencia: No se pudo cargar el sonido '{path}'. El sonido estará desactivado.")
        class DummySound:
            def play(self): pass
        return DummySound()
    try:
        return pygame.mixer.Sound(path)
    except (pygame.error, FileNotFoundError):
        print(f"Advertencia: Error al cargar el sonido '{path}'.")
        class DummySound:
            def play(self): pass
        return DummySound()

class AssetLoader:
    """Gestiona la carga y acceso a todos los assets del juego."""
    def __init__(self, checker_size):
        self.board = load_image('board.png', (1000, 700))
        self.white_checker = load_image('checker_white.png', checker_size)
        self.black_checker = load_image('checker_black.png', checker_size)

        self.dice = {
            i: load_image(f'dice_{i}.png', (50, 50)) for i in range(1, 7)
        }

        self.roll_sound = load_sound('dice_roll.wav')
        self.move_sound = load_sound('checker_move.wav')
        self.capture_sound = load_sound('checker_capture.wav')

    def get_dice_image(self, number):
        return self.dice.get(number)

    def play_roll(self):
        self.roll_sound.play()

    def play_move(self):
        self.move_sound.play()

    def play_capture(self):
        self.capture_sound.play()