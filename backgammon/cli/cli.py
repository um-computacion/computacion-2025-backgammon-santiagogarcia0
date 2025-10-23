"""
Módulo CLI
Provee una interfaz de línea de comandos básica para jugar Backgammon.
"""

from backgammon.core.player import Player
from backgammon.core.game import Game

class CLI:
    def __init__(self):
        self.game = None

    def start(self):
        print("🎲 Bienvenido a Backgammon (versión simplificada) 🎲")
        name1 = input("Nombre del Jugador 1: ")
        name2 = input("Nombre del Jugador 2: ")

        player1 = Player(name1)
        player2 = Player(name2)

        self.game = Game(player1, player2)
        self.game.start_game()

        while True:
            if self.game.is_finished():
                winner = self.game.current_player.name
                print(f"🏆 ¡{winner} ha ganado!")
                break
            self.show_menu()

    def show_menu(self):
        print("\n===== Menú =====")
        print("1. Tirar dados")
        print("2. Mover ficha")
        print("3. Mostrar estado del juego")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            roll = self.game.roll_dice()
            if roll:
                print(f"Dados: {roll}")
            else:
                print("El juego ya terminó.")

        elif opcion == "2":
            jugador = self.game.current_player
            print(f"Turno de {jugador.name}")
            try:
                from_point = int(input("Mover desde punto: "))
                to_point = int(input("Mover a punto: "))
            except ValueError:
                print("Entrada inválida, ingresa números.")
                return

            if self.game.move(from_point, to_point):
                print("Movimiento realizado ✅")
            else:
                print("Movimiento inválido ❌")

        elif opcion == "3":
            self.print_board_state()

        elif opcion == "4":
            print("👋 Gracias por jugar Backgammon!")
            exit()

        else:
            print("Opción inválida, intenta nuevamente.")

    def print_board_state(self):
        """Imprime tablero + bar + borneado."""
        print("\n=== Tablero ===")
        print(self.game.board)
        print("\n=== Bar ===")
        for player, checkers in self.game.board.bar.items():
            print(f"{player}: {len(checkers)} fichas -> {checkers}")
        print("\n=== Borneado ===")
        for player, checkers in self.game.board.borne_off.items():
            print(f"{player}: {len(checkers)} fichas borneadas")
