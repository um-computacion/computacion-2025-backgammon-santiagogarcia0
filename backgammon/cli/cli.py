"""
Módulo CLI
Provee una interfaz de línea de comandos para jugar Backgammon.
"""

from backgammon.core.game import Game

class CLI:
    def __init__(self):
        self.game = Game()

    def start(self):
        print("🎲 ¡Bienvenido a Backgammon por Consola! 🎲")
        self.game.start_game()
        
        while not self.game.is_finished():
            self.print_board_state()
            player = self.game.current_player
            print(f"\n--- Turno de {player.name} ---")

            # Tirar dados
            input("Presiona Enter para tirar los dados...")
            dice = self.game.roll_dice()
            print(f"Has sacado: {dice}")

            if not self.game.available_moves:
                print("No tienes movimientos posibles. Pasando turno.")
                continue

            # Realizar movimientos
            while self.game.available_moves:
                self.print_board_state()
                print(f"Dados disponibles: {self.game.available_moves}")
                
                try:
                    from_point_str = input("Mover desde (o 'bar'): ")
                    from_point = "bar" if from_point_str == "bar" else int(from_point_str)
                    
                    to_point = int(input("Mover hasta: "))

                    if self.game.move(from_point, to_point):
                        print("Movimiento realizado con éxito. ✅")
                    else:
                        print("Movimiento inválido. Inténtalo de nuevo. ❌")
                except ValueError:
                    print("Entrada inválida. Introduce números para los puntos.")
        
        print(f"\n¡Felicidades, {self.game.winner.name}! Has ganado. 🏆")

    def print_board_state(self):
        """Imprime el estado completo del tablero."""
        board = self.game.board
        print("\n" + "="*40)
        
        # Puntos
        for i in range(13, 25):
            print(f"{i:2}: {board.points[i]}")
        print("-" * 40)
        for i in range(12, 0, -1):
            print(f"{i:2}: {board.points[i]}")

        # Barra
        print("\nBarra:")
        for name, checkers in board.bar.items():
            if checkers:
                print(f"  {name}: {len(checkers)} fichas")

        # Fichas fuera
        print("\nFichas fuera:")
        for name, checkers in board.borne_off.items():
            print(f"  {name}: {len(checkers)} fichas")
        
        print("="*40)

if __name__ == "__main__":
    CLI().start()
