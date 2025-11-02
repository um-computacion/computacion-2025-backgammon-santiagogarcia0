 PROMPTS PARA TESTING DE CODIGO
 
 Archivo: test_board.py

 yo: Necesito ayuda para escribir un test en Python con unittest. Quiero verificar la lógica de bear-off en mi clase Board. específicamente, el caso donde un jugador saca una ficha con un dado de valor superior porque es la ficha más alejada del final. como puedo configurar el tablero en mi test para probar esto?

 Gemini: Claro. Testear estados específicos en un juego como Backgammon requiere controlar el estado del tablero manualmente. Te recomiendo que en tu método de test (o en el `setUp` si es común a varios tests) configures el tablero para que se cumplan las condiciones exactas que quieres probar.

  Para tu caso, la configuración sería:
  1.  **Vacía el tablero:** Para evitar interferencias de otras fichas, empieza limpiando el tablero.
  2.  **Coloca las fichas:** Pon una ficha del jugador en el punto más lejano que quieras probar (ej. punto 24 para el jugador blanco) y otra en un punto anterior (ej. 22). Esto es clave para poder probar que la regla no se aplica incorrectamente a la ficha del punto 22.
  3.  **Asegúrate de que el jugador puede hacer "bear-off":** Todas las fichas de ese jugador deben estar en su "home board". Al colocar las fichas manualmente como te indico, ya cumples esta condición.

  Una vez configurado, puedes llamar a `get_legal_moves` y usar `asserts` para verificar el resultado.

  Aquí te dejo un ejemplo completo de un método de test:
  ```python
  def test_get_legal_moves_bear_off_white_player(self):
      # 1. Vacía el tablero y coloca solo las fichas necesarias
      self.board.points = {i: [] for i in range(1, 25)}
      self.board.points[22] = [self.player2.name]
      self.board.points[24] = [self.player2.name] # Ficha más lejana
      
      # 2. Test de bear off con dado mayor (y es la ficha más lejana)
      # Un 3 es suficiente para sacar la ficha del 24 (necesitaría un 1)
      moves = self.board.get_legal_moves(self.player2, 24, [3])
      self.assertIn(25, moves, "Debería poder sacar la ficha más lejana con un dado mayor")

      # 3. Test de bear off inválido (no es la ficha más lejana)
      # Un 5 no debería poder sacar la ficha del 22 porque hay otra en el 24
      moves = self.board.get_legal_moves(self.player2, 22, [5])
      self.assertNotIn(25, moves, "No debería poder sacar una ficha si hay otra más lejana")
  ```
  
  Yo: quiero escribir un test para has_any_legal_move. Necesito un escenario donde un jugador tiene una ficha en la barra, saca un 1 y un 2 en los dados, pero los puntos de entrada (24 y 23 para el jugador 1) están bloqueados por el oponente. El método debería devolver `False`. Me ayudas a hacerlo?

  
  Gemini: Para este caso, necesitas manipular tres partes del estado del tablero:
  1.  `self.board.bar`: Añade una ficha del jugador 1 a la barra.
  2.  `self.board.points[24]`: Coloca dos fichas del jugador 2 para bloquear este punto.
  3.  `self.board.points[23]`: Haz lo mismo para el punto 23.

  Luego, simplemente llama a `self.board.has_any_legal_move(self.player1, [1, 2])` y verifica que el resultado es `False` con `self.assertFalse()`.

  El test se vería así:
  ```python
  def test_has_any_legal_move_from_bar_false(self):
      self.board.bar[self.player1.name] = [self.player1.name]
      self.board.points[24] = [self.player2.name, self.player2.name]
      self.board.points[23] = [self.player2.name, self.player2.name]
      self.assertFalse(self.board.has_any_legal_move(self.player1, [1, 2]))
  ```

  💡 **Qué cambió**
  Este prompt ayuda a documentar cómo probar una regla fundamental y a menudo compleja del Backgammon. La IA sugiere un setup muy limpio y específico para simular una situación de bloqueo total, lo que demuestra la importancia de controlar el estado del tablero para validar la lógica de reglas de forma aislada.

---

Archivo: test_game.py

  yo: Necesito testear un comportamiento clave en mi clase Game: si un jugador tira los dados y no tiene ningún movimiento legal posible, el turno debería pasar automáticamente al siguiente jugador. Me ayudas a ver como se puede simular eso?

  Gemini: Este es un caso de prueba excelente que requiere tanto manipulación del estado como `mocking`. La estrategia es:
  1.  **Manipular el tablero:** Coloca al jugador en una situación sin escape. Por ejemplo, pon una de sus fichas en la barra y luego bloquea todos los posibles puntos de entrada con las fichas del oponente.
  2.  **Controlar los dados con `patch`:** Usa `unittest.mock.patch` para forzar que el método `self.game.dice.roll()` devuelva una tirada específica (ej. `(1, 2)`). Esto asegura que los puntos de entrada que has bloqueado son los únicos que el jugador intentaría usar.
  3.  **Verificar el cambio de turno:** Guarda el índice del turno actual antes de llamar a `roll_dice()`, y luego usa `self.assertNotEqual()` para asegurar que el índice del turno ha cambiado después de la llamada.

  Aquí tienes un ejemplo de cómo implementar esto:
  ```python
  from unittest.mock import patch

  def test_roll_dice_and_no_legal_moves(self):
      # 1. Bloquear todos los puntos de entrada de P2
      for i in range(1, 7):
          self.game.board.points[i] = [self.player1.name] * 2
      
      # Poner una ficha de P2 en la barra
      self.game.board.bar[self.player2.name].append(self.player2.name)
      self.game.current_turn_index = 1 # Es el turno de P2
      
      initial_turn = self.game.current_turn_index
      
      # 2. Simular una tirada que no permite salir
      with patch.object(self.game.dice, 'roll', return_value=(1, 2)):
          self.game.roll_dice()
      
      # 3. El turno debería haber cambiado
      self.assertNotEqual(initial_turn, self.game.current_turn_index)
  ```

