# src/gui/drawer.py

import pygame
from . import config
from src.jogo import Jogo
from ..doenca import Cor
from ..carta import CartaCidade

class Drawer:
    # __init__, _criar_botoes_acao, draw_game, get_cidade_em_pos,
    # _draw_conexoes, _draw_elementos_mapa permanecem exatamente iguais...
    # Cole o código abaixo substituindo o original para garantir que tudo esteja incluído.

    def __init__(self, screen, jogo: Jogo):
        self.screen = screen
        self.jogo = jogo
        self.mapa_img = pygame.image.load(config.CAMINHO_IMAGEM_MAPA).convert()
        self.mapa_img = pygame.transform.scale(self.mapa_img, (config.LARGURA_TELA, config.ALTURA_TELA))
        self.botoes_acao = {}
        self.botao_finalizar_turno_rect = pygame.Rect(config.LARGURA_TELA - 180, config.ALTURA_TELA - 60, 160, 40)
        self.botoes_acao_rects = []
        self.botoes_acao_nomes = []
        self._criar_botoes_acao()

    def _criar_botoes_acao(self):
        nomes_acoes = [
            "Mover (Automóvel)", "Voo Direto", "Voo Fretado", "Ponte Aérea",
            "Construir Centro", "Tratar Doença", "Desenvolver Cura", "Compartilhar"
        ]
        pos_x = 20
        pos_y = config.ALTURA_TELA - 110
        for nome in nomes_acoes:
            self.botoes_acao_rects.append(pygame.Rect(pos_x, pos_y, 140, 30))
            self.botoes_acao_nomes.append(nome)
            pos_x += 150
            if pos_x > config.LARGURA_TELA - 150:
                pos_x = 20
                pos_y += 40
        self.botoes_acao = dict(zip(self.botoes_acao_nomes, self.botoes_acao_rects))

    def draw_game(self, acao_ativa=None, cidade_ativa=None):
        self.screen.blit(self.mapa_img, (0, 0))
        self._draw_conexoes()
        self._draw_elementos_mapa(cidade_ativa)
        self._draw_hud()
        self._draw_botoes(acao_ativa)
        pygame.display.flip()

    def get_cidade_em_pos(self, pos):
        for nome, coord in config.COORDENADAS_CIDADES.items():
            if pygame.Rect(coord[0] - 10, coord[1] - 10, 20, 20).collidepoint(pos):
                return self.jogo.mapa.get_cidade(nome)
        return None

    def _draw_conexoes(self):
        # Seu código de _draw_conexoes aqui... (sem alterações)
        for cidade in self.jogo.mapa.cidades.values():
            pos1 = config.COORDENADAS_CIDADES.get(cidade.nome)
            if pos1:
                for vizinho in cidade.vizinhos:
                    pos2 = config.COORDENADAS_CIDADES.get(vizinho.nome)
                    if (cidade.nome == "São Francisco" or cidade.nome == "Tóquio") and (vizinho.nome == "São Francisco" or vizinho.nome == "Tóquio"):
                        points = []; curve_height = 120; num_segments = 30
                        for i in range(num_segments + 1):
                            t = i / num_segments
                            x = pos1[0] * (1 - t) + pos2[0] * t
                            y = pos1[1] * (1 - t) + pos2[1] * t
                            y -= curve_height * 4 * (t - t**2)
                            points.append((x, y))
                        pygame.draw.lines(self.screen, config.VERMELHO, False, points, 2)
                    elif (cidade.nome == "São Francisco" or cidade.nome == "Manila") and (vizinho.nome == "São Francisco" or vizinho.nome == "Manila"):
                        points = []; curve_height = 215; num_segments = 30
                        for i in range(num_segments + 1):
                            t = i / num_segments
                            x = pos1[0] * (1 - t) + pos2[0] * t
                            y = pos1[1] * (1 - t) + pos2[1] * t
                            y -= curve_height * 4 * (t - t**2)
                            points.append((x, y))
                        pygame.draw.lines(self.screen, config.VERMELHO, False, points, 2)
                    elif (cidade.nome == "Los Angeles" or cidade.nome == "Sydney") and (vizinho.nome == "Los Angeles" or vizinho.nome == "Sydney"):
                        points = []; curve_height = 75; num_segments = 30
                        for i in range(num_segments + 1):
                            t = i / num_segments
                            x = pos1[0] * (1 - t) + pos2[0] * t
                            y = pos1[1] * (1 - t) + pos2[1] * t
                            y -= curve_height * 4 * (t - t**2)
                            points.append((x, y))
                        pygame.draw.lines(self.screen, config.VERMELHO, False, points, 2)
                    elif pos2:
                        pygame.draw.line(self.screen, config.AZUL, pos1, pos2, 2)

    def _draw_elementos_mapa(self, cidade_ativa):
        # Seu código de _draw_elementos_mapa aqui... (sem alterações)
        for cidade in self.jogo.mapa.cidades.values():
            pos = config.COORDENADAS_CIDADES.get(cidade.nome)
            if pos:
                cor_circulo = config.COR_DOENCA.get(cidade.cor, config.PRETO)
                raio = 12 if cidade == cidade_ativa else 8
                pygame.draw.circle(self.screen, cor_circulo, pos, raio)
                pygame.draw.circle(self.screen, config.PRETO, pos, raio, 2)
                texto_cidade = config.FONTE_CIDADE.render(cidade.nome, True, config.BRANCO)
                qtd_letras = len(cidade.nome)
                pygame.draw.rect(self.screen, (0,0,0,100), (pos[0]-(qtd_letras*3 + 5), pos[1]+10, (qtd_letras*6 + 10), 15))
                rect_texto = texto_cidade.get_rect(center=(pos[0], pos[1] + 18))
                self.screen.blit(texto_cidade, rect_texto)
                if cidade.centro_pesquisa:
                    pygame.draw.rect(self.screen, config.BRANCO, (pos[0] - 5, pos[1] - 5, 10, 10), 0)
                offset_x = -15
                for cor_cubo, quantidade in cidade.cubos.items():
                    if quantidade > 0:
                        for i in range(quantidade):
                            pygame.draw.rect(self.screen, config.PRETO, (pos[0] + offset_x - 2, pos[1] - 20 - (i * 6) - 2, 12 + 4, 5 + 4))
                            pygame.draw.rect(self.screen, config.COR_DOENCA.get(cor_cubo, config.PRETO), (pos[0] + offset_x, pos[1] - 20 - (i * 6), 12, 5))
                        offset_x += 15
        posicoes_usadas = {}
        for i, jogador in enumerate(self.jogo.jogadores):
            pos_cidade = config.COORDENADAS_CIDADES.get(jogador.cidade_atual.nome)
            if pos_cidade:
                offset = posicoes_usadas.get(pos_cidade, 0)
                cor_peao = config.COR_PEAO_JOGADOR[i % len(config.COR_PEAO_JOGADOR)]
                pos_peao = (pos_cidade[0] - 15 + offset, pos_cidade[1] - 10)
                pygame.draw.circle(self.screen, cor_peao, pos_peao, 6)
                pygame.draw.circle(self.screen, config.PRETO, pos_peao, 6, 2)
                posicoes_usadas[pos_cidade] = offset + 12
    
    # --- MÉTODO MODIFICADO ---
    def _draw_hud(self):
        pygame.draw.rect(self.screen, (0, 0, 0, 180), (0, 0, config.LARGURA_TELA, 75))
        jogador_atual = self.jogo.turno_atual.jogador_atual
        info_text = f"Turno de: {jogador_atual.nome} ({jogador_atual.personagem.nome}) | Ações restantes: {self.jogo.turno_atual.acoes_restantes} | localização: {jogador_atual.cidade_atual.nome}"
        texto = config.FONTE_PADRAO.render(info_text, True, config.BRANCO)
        self.screen.blit(texto, (20, 20))

        mao_texto_base = "Mão: "
        x_offset = 20 + config.FONTE_INFO.size(mao_texto_base)[0]
        self.screen.blit(config.FONTE_INFO.render(mao_texto_base, True, config.AMARELO_CLARO), (20, 50))

        for carta in jogador_atual.mao:
            cor_texto = config.BRANCO
            if isinstance(carta, CartaCidade):
                cor_texto = config.COR_DOENCA.get(carta.cor, config.BRANCO)
            
            nome_carta = carta.nome
            if len(nome_carta) > 12: # Abrevia nomes longos
                nome_carta = nome_carta[:10] + "..."

            texto_carta = config.FONTE_INFO.render(nome_carta, True, cor_texto)
            self.screen.blit(texto_carta, (x_offset, 50))
            x_offset += config.FONTE_INFO.size(nome_carta + ", ")[0]

        status_surtos = f"Surtos: {self.jogo.marcador_surtos} / 8"
        texto_surtos = config.FONTE_PADRAO.render(status_surtos, True, config.COR_DOENCA.get(Cor.VERMELHO, config.PRETO))
        self.screen.blit(texto_surtos, (config.LARGURA_TELA - 140, 20)) # Posição ajustada

        # --- MODIFICAÇÃO ---
        # Adiciona a chamada para o novo método que desenha o status das curas
        self._draw_status_curas()

        if self.jogo.game_over:
            self._draw_fim_de_jogo()

    # --- NOVO MÉTODO ---
    def _draw_status_curas(self):
        """Desenha os indicadores de cura das doenças."""
        pos_x = config.LARGURA_TELA - 280  # Posição inicial dos indicadores
        pos_y = 50
        
        titulo = config.FONTE_INFO.render("Curas:", True, config.BRANCO)
        self.screen.blit(titulo, (pos_x, pos_y))
        pos_x += titulo.get_width() + 15

        # Ordena para garantir que a ordem das cores seja sempre a mesma
        doencas_ordenadas = sorted(self.jogo.doencas.items(), key=lambda item: item[0].value)

        for cor, doenca in doencas_ordenadas:
            cor_pygame = config.COR_DOENCA.get(cor, config.PRETO)
            
            # Posição central do indicador
            centro_indicador = (pos_x, pos_y + 8)

            if doenca.cura_descoberta:
                # Se a cura foi descoberta, desenha um "brilho" e um símbolo
                pygame.draw.circle(self.screen, config.COR_CURA_DESCOBERTA, centro_indicador, 11)
                pygame.draw.circle(self.screen, cor_pygame, centro_indicador, 9)
                pygame.draw.circle(self.screen, config.BRANCO, centro_indicador, 3) # Símbolo de "ok"
            else:
                # Se a cura não foi descoberta, desenha um indicador simples
                pygame.draw.circle(self.screen, config.PRETO, centro_indicador, 10)
                pygame.draw.circle(self.screen, cor_pygame, centro_indicador, 9)

            pos_x += 35 # Espaçamento entre os indicadores

    def _draw_botoes(self, acao_ativa):
        # Seu código de _draw_botoes aqui... (sem alterações)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), (0, config.ALTURA_TELA - 130, config.LARGURA_TELA, 130))
        for nome, rect in self.botoes_acao.items():
            cor_botao = config.AMARELO_CLARO if nome == acao_ativa else config.CINZA
            pygame.draw.rect(self.screen, cor_botao, rect, 0, 5)
            pygame.draw.rect(self.screen, config.PRETO, rect, 2, 5)
            texto = config.FONTE_INFO.render(nome, True, config.PRETO)
            text_rect = texto.get_rect(center=rect.center)
            self.screen.blit(texto, text_rect)
        pygame.draw.rect(self.screen, config.VERDE_CLARO, self.botao_finalizar_turno_rect, 0, 5)
        texto = config.FONTE_PADRAO.render("Finalizar Turno", True, config.PRETO)
        text_rect = texto.get_rect(center=self.botao_finalizar_turno_rect.center)
        self.screen.blit(texto, text_rect)

    def _draw_fim_de_jogo(self):
        # Seu código de _draw_fim_de_jogo aqui... (sem alterações)
        s = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))
        vitoria = "vitoria" in self.jogo.mensagem_fim_jogo.lower()
        cor_titulo = config.COR_CURA_DESCOBERTA if vitoria else config.COR_DOENCA.get(Cor.VERMELHO, config.PRETO)
        texto_titulo = config.FONTE_TITULO.render("FIM DE JOGO", True, cor_titulo)
        rect_titulo = texto_titulo.get_rect(center=(config.LARGURA_TELA / 2, config.ALTURA_TELA / 2 - 30))
        self.screen.blit(texto_titulo, rect_titulo)
        texto_msg = config.FONTE_PADRAO.render(self.jogo.mensagem_fim_jogo, True, config.BRANCO)
        rect_msg = texto_msg.get_rect(center=(config.LARGURA_TELA / 2, config.ALTURA_TELA / 2 + 20))
        self.screen.blit(texto_msg, rect_msg)
    
    def get_jogador_em_pos(self, pos):
        """Verifica se um clique ocorreu na posição de um jogador e retorna o objeto Jogador."""
        posicoes_usadas = {}
        for i, jogador in enumerate(self.jogo.jogadores):
            pos_cidade = config.COORDENADAS_CIDADES.get(jogador.cidade_atual.nome)
            if pos_cidade:
                offset = posicoes_usadas.get(pos_cidade, 0)
                pos_peao = (pos_cidade[0] - 15 + offset, pos_cidade[1] - 10)
                # Cria um retângulo ao redor do peão para checar a colisão
                raio_clique = 8 
                rect_peao = pygame.Rect(pos_peao[0] - raio_clique, pos_peao[1] - raio_clique, raio_clique * 2, raio_clique * 2)
                
                if rect_peao.collidepoint(pos):
                    return jogador
                posicoes_usadas[pos_cidade] = offset + 12
        return None