# Backgammon

Autor: Santiago García

Proyecto de implementación del juego Backgammon en Python.

## Funcionalidades actuales
- CLI (línea de comando) inicial con menú simple:
  - Tirar dados
  - Mover fichas
  - Mostrar estado del tablero
- Clases centrales implementadas: `Game`, `Board`, `Player`, `Dice`
- Gestión de turnos y tiradas de dados
- Setup inicial del tablero
- Pruebas unitarias básicas para `Board`, `Game` y `Player`

## Estructura del proyecto
/backgammon/
├── core/           → lógica del juego (Game, Board, Player, Dice)
├── cli/            → interfaz de consola
├── pygame_ui/      → interfaz gráfica (en desarrollo)
├── assets/         → recursos (imágenes, sonidos)
├── tests/          → pruebas unitarias
└── requirements.txt

## Cómo ejecutar (CLI)
Ejemplo simplificado para probar el flujo básico desde la consola:
```python
from backgammon.cli.cli import CLI

cli = CLI()
cli.run()
