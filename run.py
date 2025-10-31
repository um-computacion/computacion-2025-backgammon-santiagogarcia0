"""
Lanzador principal para el juego de Backgammon.
Permite al usuario elegir entre la interfaz gráfica (GUI) o la de consola (CLI).
"""

def main():
    """Función principal que maneja la selección del modo de juego."""
    print("🎲 Bienvenido a Backgammon 🎲")
    print("Elige el modo de juego:")
    print("1. Jugar con Interfaz Gráfica (Pygame)")
    print("2. Jugar en la Consola (CLI)")

    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Introduce 1 o 2: ")

    if choice == "1":
        try:
            from backgammon.pygame_ui.gui_main import PygameBackgammon
            print("Iniciando la interfaz gráfica...")
            PygameBackgammon().run()
        except ImportError as e:
            print("\nError: Parece que Pygame no está instalado.")
            print("Por favor, instálalo con: pip install pygame")
            print(f"Detalle del error: {e}")
        except Exception as e:
            print(f"\nOcurrió un error al iniciar la interfaz gráfica: {e}")
            
    elif choice == "2":
        from backgammon.cli.cli import CLI
        print("Iniciando la versión de consola...")
        CLI().start()

if __name__ == "__main__":
    main()
