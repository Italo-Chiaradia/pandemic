# src/gui/game_controller.py

import pygame
from . import config
from .drawer import Drawer
from ..jogo import Jogo
from ..acao import MoverAutomovel, VooDireto, VooFretado, PonteAerea, ConstruirCentro, TratarDoenca, DesenvolverCura, Compartilhar
from ..doenca import Cor
from ..carta import CartaCidade

class GameController:
    def __init__(self, num_players: int):
        pygame.init()
        self.screen = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
        pygame.display.set_caption("Pandemic - Estrutura Original")

        self.jogo = Jogo(num_players=num_players, dificuldade='iniciante')
        self.drawer = Drawer(self.screen, self.jogo)
        
        self.clock = pygame.time.Clock()
        self.running = True

        # --- ESTADOS MODIFICADOS PARA CONTROLAR A INTERFACE ---
        self.cidade_selecionada = None
        self.acao_selecionada = None
        
        # Novas variáveis para controlar ações de múltiplos cliques
        self.aguardando_selecao_de_alvo = False
        self.tipo_de_alvo = None # Ex: "jogador", "cidade"
        # -----------------------------------------------------------

    def run_game(self):
        while self.running:
            self.clock.tick(config.FPS)
            self.handle_events()
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.jogo.game_over:
                pos = pygame.mouse.get_pos()
                self._handle_click(pos)

    def draw(self):
        # O Drawer agora lê do self.jogo para desenhar tudo
        self.drawer.draw_game(self.acao_selecionada, self.cidade_selecionada)

    def _resetar_selecao_acao(self):
        """Função auxiliar para limpar o estado da seleção."""
        self.acao_selecionada = None
        self.cidade_selecionada = None
        self.aguardando_selecao_de_alvo = False
        self.tipo_de_alvo = None

    def _handle_click(self, pos):
        # --- PARTE 1: LÓGICA DE SELEÇÃO DE ALVO (SEGUNDO CLIQUE) ---
        if self.aguardando_selecao_de_alvo:
            if self.tipo_de_alvo == "jogador_para_compartilhar":
                jogador_alvo = self.drawer.get_jogador_em_pos(pos)
                jogador_atual = self.jogo.turno_atual.jogador_atual
                
                # Verifica se o clique foi em um jogador válido
                if jogador_alvo and jogador_alvo != jogador_atual and jogador_alvo.cidade_atual == jogador_atual.cidade_atual:
                    print(f"Alvo selecionado para compartilhar: {jogador_alvo.nome}")
                    
                    # Tenta encontrar a carta necessária para a troca
                    carta_para_dar = next((c for c in jogador_atual.mao if isinstance(c, CartaCidade) and c.nome == jogador_atual.cidade_atual.nome), None)
                    
                    if carta_para_dar:
                        self.jogo.turno_atual.realizar_acao(
                            Compartilhar(),
                            outro_jogador=jogador_alvo,
                            carta=carta_para_dar,
                            tipo="dar"
                        )
                    else:
                        print(f"Você não tem a carta de {jogador_atual.cidade_atual.nome} para compartilhar.")

                    self._resetar_selecao_acao() # Finaliza a ação
                else:
                    print("Seleção inválida. Clique cancelado. Escolha uma ação novamente.")
                    self._resetar_selecao_acao() # Cancela a ação
            return # Impede que o resto do código de clique seja executado

        # --- PARTE 2: LÓGICA DE SELEÇÃO DE AÇÃO (PRIMEIRO CLIQUE) ---
        
        # 2.1. Checa cliques nos botões de ação
        for nome_acao, rect in self.drawer.botoes_acao.items():
            if rect.collidepoint(pos):
                print(f"Botão de ação '{nome_acao}' clicado.")
                self._resetar_selecao_acao() # Reseta qualquer ação anterior
                self.acao_selecionada = nome_acao

                # --- LÓGICA DE ATIVAÇÃO DO MODO DE SELEÇÃO ---
                if self.acao_selecionada == "Compartilhar":
                    self.aguardando_selecao_de_alvo = True
                    self.tipo_de_alvo = "jogador_para_compartilhar"
                    print("Modo 'Compartilhar': Por favor, clique no jogador com quem deseja trocar a carta.")
                
                return # Sai da função após clicar em um botão de ação

        # 2.2. Checa clique no botão de finalizar turno
        if self.drawer.botao_finalizar_turno_rect.collidepoint(pos):
            print("Botão 'Finalizar Turno' clicado.")
            self.jogo.turno_atual.finalizar_fase_acoes()
            self._resetar_selecao_acao()
            return

        # 2.3. Lógica de clique no mapa (para ações que precisam de uma cidade)
        cidade_clicada = self.drawer.get_cidade_em_pos(pos)
        if cidade_clicada and self.acao_selecionada:
            sucesso = False
            jogador_atual = self.jogo.turno_atual.jogador_atual
            
            if self.acao_selecionada == "Mover (Automóvel)":
                sucesso = self.jogo.turno_atual.realizar_acao(MoverAutomovel(), destino=cidade_clicada)
            elif self.acao_selecionada == "Voo Direto":
                sucesso = self.jogo.turno_atual.realizar_acao(VooDireto(), destino=cidade_clicada)
            elif self.acao_selecionada == "Voo Fretado":
                sucesso = self.jogo.turno_atual.realizar_acao(VooFretado(), destino=cidade_clicada)
            elif self.acao_selecionada == "Ponte Aérea":
                sucesso = self.jogo.turno_atual.realizar_acao(PonteAerea(), destino=cidade_clicada)
            elif self.acao_selecionada == "Construir Centro":
                if cidade_clicada == jogador_atual.cidade_atual:
                    sucesso = self.jogo.turno_atual.realizar_acao(ConstruirCentro())
            elif self.acao_selecionada == "Tratar Doença":
                if cidade_clicada == jogador_atual.cidade_atual:
                    sucesso = self.jogo.turno_atual.realizar_acao(TratarDoenca(), cor=cidade_clicada.cor)
            elif self.acao_selecionada == "Desenvolver Cura":
                cor_para_curar = jogador_atual.cidade_atual.cor
                sucesso = self.jogo.turno_atual.realizar_acao(DesenvolverCura(), cor=cor_para_curar)

            if sucesso:
                self._resetar_selecao_acao() # Reseta a ação após o sucesso