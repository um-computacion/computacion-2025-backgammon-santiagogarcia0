# Justificación del Diseño del Proyecto Backgammon

Este documento detalla las decisiones de arquitectura y diseño tomadas durante el desarrollo del juego de Backgammon.

## 1. Resumen del Diseño General

El proyecto sigue una arquitectura en capas que separa la lógica del juego de su presentación. Este diseño se divide en dos componentes principales:

1.  **Núcleo del Juego (`backgammon/core`):** Es el corazón del proyecto. Contiene toda la lógica, las reglas y el estado del juego de Backgammon. Es completamente independiente y no tiene conocimiento de cómo se mostrará el juego al usuario. Actúa como el **Modelo** en un patrón MVC (Modelo-Vista-Controlador).
2.  **Capas de Interfaz (`backgammon/cli` y `backgammon/pygame_ui`):** Son los "clientes" del núcleo. Se encargan de presentar el estado del juego al usuario y de recoger sus entradas. Actualmente, existen dos implementaciones: una para la línea de comandos (CLI) y otra gráfica (Pygame). Actúan como la **Vista** y el **Controlador**.

Esta separación es la decisión de diseño más importante, ya que permite añadir nuevas interfaces (por ejemplo, una web) en el futuro sin modificar una sola línea de la lógica del juego.

## 2. Justificación de las Clases Elegidas

Las clases del núcleo fueron diseñadas siguiendo el Principio de Responsabilidad Única.

-   **`Game`**: Es la clase orquestadora. Su única responsabilidad es gestionar el flujo de una partida. Controla los turnos, inicia el juego, gestiona las tiradas de dados y verifica si hay un ganador. No conoce las reglas de movimiento, solo le pide al `Board` que los valide y ejecute.
-   **`Board`**: Representa el estado del tablero. Su responsabilidad es saber dónde está cada ficha en todo momento. Contiene toda la lógica de las reglas de movimiento (`get_legal_moves`), incluyendo las más complejas como el "hit", el reingreso desde la barra y el "bear-off".
-   **`Player`**: Es una estructura de datos simple que representa a un jugador. Su responsabilidad es mantener la información asociada a un jugador, como su nombre.
-   **`Dice`**: Es una clase de utilidad simple cuya única responsabilidad es generar y proveer los resultados de una tirada de dados.

## 3. Justificación de Atributos Principales

-   **`Board.points` (`dict`):** Se eligió un diccionario `{int: list[str]}` para representar los 24 puntos del tablero. La clave es el número del punto y el valor es una lista de strings con los nombres de los jugadores que tienen fichas allí. Usar strings (`player.name`) en lugar de objetos `Player` simplifica la estructura, evita referencias circulares y facilita la serialización si fuera necesario en el futuro.
-   **`Game.available_moves` (`list`):** Una lista de enteros que representa los dados que el jugador actual aún puede usar. Cada vez que se realiza un movimiento, el valor del dado correspondiente se elimina de esta lista. Esto permite gestionar de forma sencilla los dobles (cuatro movimientos) y el consumo de dados.
-   **`Player.direction` (`int`):** Un atributo que vale `1` o `-1`. Permite que la lógica de cálculo de movimientos (`to_point = from_point + roll * direction`) sea genérica y funcione para ambos jugadores sin necesidad de código duplicado.

## 4. Decisiones de Diseño Relevantes

-   **Separación de Lógica y Presentación:** Como se mencionó, el núcleo (`core`) es agnóstico a la interfaz. Esto permite que el `Game` pueda ser controlado tanto por un humano (a través de la CLI o Pygame) como por una IA en el futuro.
-   **Callback `on_turn_change`:** La clase `Game` acepta una función opcional `on_turn_change` en su constructor. La GUI de Pygame le pasa una función a este *callback*. Cuando el `Game` cambia de turno (por ejemplo, porque un jugador se queda sin movimientos), llama a esta función. Esto permite a la lógica notificar a la interfaz de un evento importante sin estar directamente acoplada a ella (Inversión de Control).

## 5. Excepciones y Manejo de Errores

El manejo de errores se concentra en los puntos de interacción con el usuario o el entorno:

-   **`run.py`**: Utiliza un bloque `try...except ImportError` para detectar si `pygame` no está instalado y mostrar un mensaje amigable al usuario, en lugar de fallar con un error no controlado.
-   **`cli.py`**: Utiliza un bloque `try...except ValueError` para capturar entradas no numéricas del usuario al mover las fichas, evitando que el programa se cierre inesperadamente.

## 6. Estrategias de Testing y Cobertura

La estrategia de testing se centra en garantizar la robustez de la lógica del juego.

-   **Enfoque en Tests Unitarios:** Las pruebas se concentran al 100% en el núcleo (`core`), ya que contiene las reglas de negocio y es la parte más crítica del sistema. Las interfaces, al tener una lógica mínima, no son el foco principal.
-   **Aislamiento de Casos de Prueba:** Los tests manipulan directamente el estado del `Board` (`self.board.points = ...`) para crear escenarios muy específicos que serían difíciles de alcanzar en una partida normal. Esto permite probar reglas complejas (como el "bear-off" con un dado de valor superior) de forma aislada y determinista.
-   **Uso de Mocks:** En `test_game.py`, se utiliza `unittest.mock.patch` para simular tiradas de dados. Esto elimina el azar de las pruebas y permite verificar cómo reacciona el juego ante resultados específicos (por ejemplo, un doble o una tirada que no permite movimientos).

## 7. Cumplimiento de Principios SOLID

El diseño del núcleo adhiere principalmente al **Principio de Responsabilidad Única (SRP)**:

-   `Game`: Su única razón para cambiar es si cambia el flujo del juego (ej. añadir una regla de apuestas).
-   `Board`: Su única razón para cambiar es si cambian las reglas de movimiento del Backgammon.
-   `Dice`: Su única razón para cambiar es si cambia la forma en que se tiran los dados.
-   Las clases de UI/CLI: Su única razón para cambiar es si cambia la forma de presentar la información o de interactuar con el usuario.

## 8. Anexos

### Diagrama de Clases (UML en Texto)

```
+----------------+          +----------------+          +----------------+
|      Game      |<>--------|     Board      |          |      Dice      |
+----------------+          +----------------+          +----------------+
| - board        |          | - points: dict |          | - last_roll    |
| - dice         |          | - bar: dict    |          +----------------+
| - players: list|          | - borne_off: dict|          | + roll()       |
| - current_turn |          +----------------+          +----------------+
+----------------+          | + setup_board()|
| + start_game() |          | + get_legal_moves()|
| + roll_dice()  |          | + move_checker() |
| + move()       |          +----------------+
| + next_turn()  |
+----------------+
       |
       |<>
       |
+----------------+
|     Player     |
+----------------+
| - name: str    |
| - direction: int|
+----------------+
```