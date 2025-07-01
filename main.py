# main.py

# MODIFICADO: O import deve ser absoluto a partir do diretório raiz do projeto.
from src.gui.game_controller import GameController

def main():
    """
    Função principal que gerencia o fluxo do jogo.
    """
    player_count = 0
    while player_count not in [2, 3, 4]:
        try:
            print("Hello from the pygame community. https://www.pygame.org/contribute.html")
            player_count_str = input("Quantos jogadores irão jogar (2-4)? ")
            player_count = int(player_count_str)
        except ValueError:
            print("Por favor, insira um número válido.")

    print(f"Iniciando um jogo para {player_count} jogadores...")

    game_controller = GameController(num_players=player_count)
    game_controller.run_game()

if __name__ == '__main__':
    main()