# Backgammon

Autor: Santiago García

Proyecto de implementación del juego Backgammon en Python.

## Funcionalidades actuales

- **CLI (línea de comando) interactiva**:
  - Tirar dados
  - Mover fichas indicando punto de origen y destino
  - Mostrar tablero, bar y borneado
  - Detección de victoria al bornear todas las fichas
  - Menú simple y dinámico por turnos

- **Clases centrales implementadas**:
  - `Game`: controla flujo del juego, turnos, tiradas y condición de fin de partida
  - `Board`: administra puntos, bar, borneado y validación de movimientos
  - `Player`: representa a los jugadores
  - `Dice`: simula los dados con soporte para dobles

- **Reglas implementadas (simplificadas)**:
  - Validación de movimientos según dados
  - Movimiento obligatorio desde puntos propios
  - Captura de fichas solitarias del oponente (hit → ficha al bar)
  - Sistema de bar para fichas capturadas
  - Borneado de fichas al llegar a la meta
  - Gestión de turnos alternados y consumo de tiradas

- **Pruebas unitarias**:
  - `Board`: validación de movimientos, hits, bar y borneado
  - `Game`: control de turnos, tiradas y condición de fin
  - `CLI`: simulación básica de interacción con menú
  - Cobertura ampliada para nuevas reglas

## Estructura del proyecto
/backgammon/
├── core/           → lógica del juego (Game, Board, Player, Dice)
├── cli/            → interfaz de consola
├── pygame_ui/      → interfaz gráfica (en desarrollo)
├── assets/         → recursos (imágenes, sonidos)
├── tests/          → pruebas unitarias
└── requirements.txt

## Cómo Poner en Funcionamiento

### Modo Juego
Para jugar, ejecuta el archivo `run.py` desde la raíz del repositorio. Se te dará a elegir entre dos interfaces:

1.  **Interfaz Gráfica (Pygame):** Una experiencia visual e interactiva.
2.  **Consola (CLI):** Una versión basada en texto, ideal para entornos sin entorno gráfico.

```bash
python3 run.py
```

### Modo Testing
Para verificar que toda la lógica del juego funciona correctamente, puedes ejecutar la suite de pruebas unitarias. Asegúrate de estar en la raíz del repositorio.

El comando buscará y ejecutará todos los tests ubicados en el directorio `tests/`.

```bash
python3 -m unittest discover tests
```