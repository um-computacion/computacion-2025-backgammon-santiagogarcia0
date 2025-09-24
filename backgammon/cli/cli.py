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
            self.show_menu()

    def show_menu(self):
        print("\n===== Menú =====")
        print("1. Tirar dados")
        print("2. Mover ficha")
        print("3. Mostrar tablero")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            roll = self.game.roll_dice()
            print(f"Dados: {roll}")

        elif opcion == "2":
            jugador = self.game.current_player
            print(f"Turno de {jugador.name}")
            from_point = int(input("Mover desde punto: "))
            to_point = int(input("Mover a punto: "))
            moved = self.game.move(from_point, to_point)
            if moved:
                print("Movimiento realizado ✅")
            else:
                print("Movimiento inválido ❌")

        elif opcion == "3":
            print(self.game.board)

        elif opcion == "4":
            print("👋 Gracias por jugar Backgammon!")
            exit()
        else:
            print("Opción inválida, intenta nuevamente.")
