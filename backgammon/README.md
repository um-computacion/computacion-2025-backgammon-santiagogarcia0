# Backgammon

Autor: Santiago García

Proyecto de implementación del juego Backgammon en Python.

## Funcionalidades actuales
- CLI (línea de comando) simplificada
- Clases centrales implementadas: `Game`, `Board`, `Player`, `Dice`
- Setup inicial de tablero y turnos

## Estructura del proyecto
/backgammon/
├── core/           → lógica del juego (Game, Board, Player, Dice)
├── cli/            → interfaz de consola
├── pygame_ui/      → interfaz gráfica (en desarrollo)
├── assets/         → recursos (imágenes, sonidos)
├── tests/          → pruebas unitarias
└── requirements.txt

## Cómo ejecutar (CLI)
Ejemplo simplificado para probar el flujo básico:
```python
from core.game import Game

game = Game()
game.start_game()                   # Inicializa tablero
player = game.get_current_player()  # Obtiene jugador actual
dice = game.roll_dice()             # Lanza dados
game.next_turn()                     # Cambia de turno
