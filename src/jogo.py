# src/jogo.py

import random
from .mapa import Mapa
from .doenca import Doenca, Cor
from .baralho import Baralho
from .carta import CartaCidade, CartaInfeccao, CartaEvento, CartaEpidemia
from .cidade import Cidade
from .jogador import Jogador
# MODIFICADO: Importa o novo personagem
from .personagem import Cientista, Medico, Pesquisadora, EspecialistaOperacoes, EspecialistaQuarentena
from .turno import Turno

class Jogo:
    # ... (métodos __init__ e outros permanecem os mesmos até _criar_jogadores)

    def _criar_jogadores(self, nomes: list[str]) -> list[Jogador]:
        # MODIFICADO: Adiciona o novo personagem à lista de disponíveis
        personagens_disponiveis = [
            Cientista(), Medico(), Pesquisadora(), EspecialistaOperacoes(), EspecialistaQuarentena()
        ]
        random.shuffle(personagens_disponiveis)
        
        jogadores = []
        cidade_inicial = self.mapa.get_cidade("Atlanta")
        for i, nome in enumerate(nomes):
            # Garante que não teremos erro se houver mais jogadores que personagens definidos
            personagem = personagens_disponiveis[i % len(personagens_disponiveis)]
            jogador = Jogador(nome, personagem, self)
            jogador.set_cidade_atual(cidade_inicial)
            jogadores.append(jogador)
            print(f"{nome} é o(a) {personagem.nome}.")
        return jogadores

    # ... (o resto do código da classe Jogo permanece o mesmo)
    def __init__(self, num_players: int, dificuldade: str = 'iniciante'):
        print(f"==== INICIANDO JOGO PANDEMIC PARA {num_players} JOGADORES ({dificuldade}) ====")
        self.num_players = num_players
        self.game_over = False
        self.mensagem_fim_jogo = ""

        # NOVO: Estado do jogo
        self.marcador_surtos = 0
        self.marcador_velocidade_infeccao = 0 # índice da lista abaixo
        self.trilha_velocidade_infeccao = [2, 2, 2, 3, 3, 4, 4]
        self.centros_pesquisa = set()
        self.max_centros_pesquisa = 6

        self.doencas = {cor: Doenca(cor) for cor in Cor}
        self.mapa = self._inicializar_mapa()

        # Configuração dos baralhos
        cartas_jogador, cartas_infeccao = self._criar_cartas_cidade()
        self.baralho_jogador = self._preparar_baralho_jogador(cartas_jogador, dificuldade)
        self.baralho_infeccao = Baralho("Infecção", cartas_infeccao)

        # Configuração dos jogadores
        self.jogadores = self._criar_jogadores([f"Jogador {i+1}" for i in range(num_players)])
        self._distribuir_cartas_iniciais()
        self.id_jogador_atual = self._definir_primeiro_jogador()

        # Configuração inicial do tabuleiro
        self._infeccao_inicial()

        self.turno_atual: Turno | None = None
        self.iniciar_novo_turno()
        print("\n==== JOGO PRONTO PARA COMEÇAR ====")

    def _inicializar_mapa(self) -> Mapa:
        mapa = Mapa()
        # DADOS COMPLETOS DO JOGO PADRÃO
        cidades_data = [
            ("São Francisco", Cor.AZUL, 883305), ("Chicago", Cor.AZUL, 2705994), ("Atlanta", Cor.AZUL, 498044),
            ("Montreal", Cor.AZUL, 1780000), ("Nova Iorque", Cor.AZUL, 8398748), ("Washington", Cor.AZUL, 705749),
            ("Londres", Cor.AZUL, 8982000), ("Madri", Cor.AZUL, 3223334), ("Paris", Cor.AZUL, 2141000),
            ("Milão", Cor.AZUL, 1352000), ("Essen", Cor.AZUL, 583109), ("São Petersburgo", Cor.AZUL, 5383000),
            ("Los Angeles", Cor.AMARELO, 3990456), ("Cidade do México", Cor.AMARELO, 9209944), ("Miami", Cor.AMARELO, 467963),
            ("Bogotá", Cor.AMARELO, 7412566), ("Lima", Cor.AMARELO, 9752000), ("Santiago", Cor.AMARELO, 5220161),
            ("Buenos Aires", Cor.AMARELO, 2891000), ("São Paulo", Cor.AMARELO, 12252023), ("Lagos", Cor.AMARELO, 14800000),
            ("Kinshasa", Cor.AMARELO, 14300000), ("Joanesburgo", Cor.AMARELO, 5635000), ("Khartoum", Cor.AMARELO, 5274000),
            ("Argel", Cor.PRETO, 3915000), ("Cairo", Cor.PRETO, 9845000), ("Istambul", Cor.PRETO, 15460000),
            ("Moscou", Cor.PRETO, 12506468), ("Bagdá", Cor.PRETO, 7665000), ("Riad", Cor.PRETO, 7676654),
            ("Teerã", Cor.PRETO, 8693706), ("Karachi", Cor.PRETO, 14916456), ("Mumbai", Cor.PRETO, 20185000),
            ("Deli", Cor.PRETO, 18980000), ("Calcutá", Cor.PRETO, 4496694), ("Chenai", Cor.PRETO, 7088000),
            ("Pequim", Cor.VERMELHO, 21540000), ("Seul", Cor.VERMELHO, 9776000), ("Xangai", Cor.VERMELHO, 26320000),
            ("Tóquio", Cor.VERMELHO, 13929000), ("Osaka", Cor.VERMELHO, 2691000), ("Taipé", Cor.VERMELHO, 2646204),
            ("Hong Kong", Cor.VERMELHO, 7482500), ("Manila", Cor.VERMELHO, 1780148), ("Bangkok", Cor.VERMELHO, 10539000),
            ("Cidade de Ho Chi Minh", Cor.VERMELHO, 8993000), ("Jacarta", Cor.VERMELHO, 10562000), ("Sydney", Cor.VERMELHO, 5312163)
        ]
        for nome, cor, pop in cidades_data:
            mapa.adicionar_cidade(Cidade(nome, cor, pop))

        conexoes = [
            ("São Francisco", "Los Angeles"), ("São Francisco", "Chicago"), ("São Francisco", "Tóquio"), ("São Francisco", "Manila"),
            ("Chicago", "Atlanta"), ("Chicago", "Montreal"), ("Chicago", "Cidade do México"), ("Chicago", "Los Angeles"),
            ("Montreal", "Nova Iorque"), ("Montreal", "Washington"),
            ("Nova Iorque", "Washington"), ("Nova Iorque", "Madri"), ("Nova Iorque", "Londres"),
            ("Atlanta", "Washington"), ("Atlanta", "Miami"),
            ("Washington", "Miami"),
            ("Los Angeles", "Sydney"), ("Los Angeles", "Cidade do México"),
            ("Cidade do México", "Miami"), ("Cidade do México", "Bogotá"), ("Cidade do México", "Lima"),
            ("Miami", "Bogotá"),
            ("Bogotá", "Lima"), ("Bogotá", "São Paulo"), ("Bogotá", "Buenos Aires"),
            ("Lima", "Santiago"),
            ("Santiago", "Buenos Aires"),
            ("Buenos Aires", "São Paulo"),
            ("São Paulo", "Madri"), ("São Paulo", "Lagos"),
            ("Lagos", "Khartoum"), ("Lagos", "Kinshasa"),
            ("Khartoum", "Cairo"), ("Khartoum", "Joanesburgo"), ("Khartoum", "Kinshasa"),
            ("Kinshasa", "Joanesburgo"),
            ("Londres", "Paris"), ("Londres", "Essen"), ("Londres", "Madri"),
            ("Madri", "Paris"), ("Madri", "Argel"),
            ("Paris", "Essen"), ("Paris", "Milão"), ("Paris", "Argel"),
            ("Essen", "Milão"), ("Essen", "São Petersburgo"),
            ("Milão", "Istambul"),
            ("São Petersburgo", "Istambul"), ("São Petersburgo", "Moscou"),
            ("Argel", "Cairo"), ("Argel", "Istambul"),
            ("Cairo", "Istambul"), ("Cairo", "Bagdá"), ("Cairo", "Riad"),
            ("Istambul", "Bagdá"), ("Istambul", "Moscou"),
            ("Moscou", "Teerã"),
            ("Bagdá", "Teerã"), ("Bagdá", "Karachi"), ("Bagdá", "Riad"),
            ("Riad", "Karachi"),
            ("Teerã", "Deli"), ("Teerã", "Karachi"),
            ("Karachi", "Mumbai"), ("Karachi", "Deli"),
            ("Mumbai", "Chenai"), ("Mumbai", "Deli"),
            ("Deli", "Chenai"), ("Deli", "Calcutá"),
            ("Chenai", "Calcutá"), ("Chenai", "Bangkok"), ("Chenai", "Jacarta"),
            ("Calcutá", "Hong Kong"), ("Calcutá", "Bangkok"),
            ("Bangkok", "Hong Kong"), ("Bangkok", "Cidade de Ho Chi Minh"), ("Bangkok", "Jacarta"),
            ("Jacarta", "Sydney"), ("Jacarta", "Cidade de Ho Chi Minh"),
            ("Cidade de Ho Chi Minh", "Manila"), ("Cidade de Ho Chi Minh", "Hong Kong"),
            ("Sydney", "Manila"),
            ("Manila", "Hong Kong"), ("Manila", "Taipé"),
            ("Hong Kong", "Xangai"), ("Hong Kong", "Pequim"), ("Hong Kong", "Taipé"),
            ("Taipé", "Xangai"), ("Taipé", "Osaka"),
            ("Pequim", "Seul"), ("Pequim", "Xangai"),
            ("Seul", "Tóquio"), ("Seul", "Xangai"),
            ("Xangai", "Tóquio"), ("Xangai", "Osaka"),
            ("Tóquio", "Osaka"),
        ]

        for c1, c2 in conexoes:
            mapa.get_cidade(c1).adicionar_vizinho(mapa.get_cidade(c2))

        # Adiciona o primeiro centro de pesquisa
        cidade_inicial = mapa.get_cidade("Atlanta")
        cidade_inicial.centro_pesquisa = True
        self.centros_pesquisa.add(cidade_inicial)
        return mapa

    def _criar_cartas_cidade(self) -> tuple[list[CartaCidade], list[CartaInfeccao]]:
        cartas_jogador = []
        cartas_infeccao = []
        for nome, cidade_obj in self.mapa.cidades.items():
            cartas_jogador.append(CartaCidade(nome, cidade_obj.cor, cidade_obj.populacao))
            cartas_infeccao.append(CartaInfeccao(nome, cidade_obj.cor, cidade_obj.populacao))
        return cartas_jogador, cartas_infeccao

    def _preparar_baralho_jogador(self, cartas_cidade, dificuldade):
        # O baralho final agora é apenas a lista de cartas de cidade.
        baralho_final = cartas_cidade
        
        # Embaralhamos as cartas de cidade para garantir a aleatoriedade.
        random.shuffle(baralho_final)

        return Baralho("Jogador", baralho_final)
    

    def _distribuir_cartas_iniciais(self):
        num_cartas_map = {2: 4, 3: 3, 4: 2}
        num_cartas = num_cartas_map[self.num_players]
        for jogador in self.jogadores:
            for _ in range(num_cartas):
                jogador.adicionar_carta_mao(self.baralho_jogador.comprar())

    def _definir_primeiro_jogador(self):
        maior_pop = -1
        primeiro_jogador_id = 0
        for i, jogador in enumerate(self.jogadores):
            for carta in jogador.mao:
                if isinstance(carta, CartaCidade):
                    if carta.populacao > maior_pop:
                        maior_pop = carta.populacao
                        primeiro_jogador_id = i
        print(f"O primeiro a jogar é {self.jogadores[primeiro_jogador_id].nome}.")
        return primeiro_jogador_id
    def _infeccao_inicial(self):
        print("\n--- Infecção Inicial ---")
        # 3 cidades com 3 cubos
        print("Fase 1: 3 cidades com 3 cubos.")
        for _ in range(3):
            carta = self.baralho_infeccao.comprar()
            cidade = self.mapa.get_cidade(carta.nome)
            for i in range(3): cidade.adicionar_cubo(cidade.cor, self, set())
            self.baralho_infeccao.descartar(carta)
        # 3 cidades com 2 cubos
        print("Fase 2: 3 cidades com 2 cubos.")
        for _ in range(3):
            carta = self.baralho_infeccao.comprar()
            cidade = self.mapa.get_cidade(carta.nome)
            for i in range(2): cidade.adicionar_cubo(cidade.cor, self, set())
            self.baralho_infeccao.descartar(carta)
        # 3 cidades com 1 cubo
        print("Fase 3: 3 cidades com 1 cubo.")
        for _ in range(3):
            carta = self.baralho_infeccao.comprar()
            cidade = self.mapa.get_cidade(carta.nome)
            cidade.adicionar_cubo(cidade.cor, self, set())
            self.baralho_infeccao.descartar(carta)

    def get_taxa_infeccao(self) -> int:
        return self.trilha_velocidade_infeccao[self.marcador_velocidade_infeccao]

    def epidemia(self):
        if self.game_over: return
        print("AUMENTO: Marcador de velocidade de infecção avança.")
        if self.marcador_velocidade_infeccao < len(self.trilha_velocidade_infeccao) - 1:
            self.marcador_velocidade_infeccao += 1
        
        print("INFECÇÃO: Comprando carta do fundo do baralho de infecção.")
        carta = self.baralho_infeccao.comprar_de_baixo()
        if carta:
            cidade = self.mapa.get_cidade(carta.nome)
            if not self.doencas[cidade.cor].erradicada:
                print(f"A epidemia atinge {cidade.nome}!")
                # Adiciona até 3 cubos ou causa um surto
                # MODIFICADO: A chamada agora passa um novo conjunto vazio para iniciar a cadeia.
                for _ in range(3):
                    cidade.adicionar_cubo(cidade.cor, self, set())
                    if cidade.cubos[cidade.cor] == 3: break # Para de adicionar se já chegou a 3
                    if self.game_over: return

            self.baralho_infeccao.descartar(carta)

        print("INTENSIDADE: Embaralhando o descarte de infecção no topo do baralho.")
        self.baralho_infeccao.intensificar()

    def surto(self, cidade_origem: Cidade, cor: Cor, cidades_ja_surtaram: set):
        if cidade_origem in cidades_ja_surtaram:
            return
        
        print(f"SURTO em {cidade_origem.nome} com a cor {cor.value}!")
        cidades_ja_surtaram.add(cidade_origem)
        
        self.marcador_surtos += 1
        if self.marcador_surtos >= 8:
            self.fim_de_jogo("derrota_surtos", "O pânico tomou conta do mundo! (8 surtos)")
            return

        for vizinho in cidade_origem.vizinhos:
            # A chamada aqui está correta, passando o conjunto para o próximo nível da cadeia
            vizinho.adicionar_cubo(cor, self, cidades_ja_surtaram)
            if self.game_over: return

    def gerenciar_centros_pesquisa(self, cidade: Cidade):
        self.centros_pesquisa.add(cidade)
        if len(self.centros_pesquisa) > self.max_centros_pesquisa:
            for c in list(self.centros_pesquisa):
                if c.nome != "Atlanta":
                    c.centro_pesquisa = False
                    self.centros_pesquisa.remove(c)
                    print(f"Limite de Centros de Pesquisa excedido. O centro em {c.nome} foi removido.")
                    break
    
    def fim_de_jogo(self, tipo: str, mensagem: str):
        if not self.game_over:
            self.game_over = True
            self.mensagem_fim_jogo = mensagem
            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"FIM DE JOGO: {mensagem}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def iniciar_novo_turno(self):
        if self.game_over: return
        jogador = self.jogadores[self.id_jogador_atual]
        self.turno_atual = Turno(jogador, self)
        print(f"\n================ NOVO TURNO: {jogador.nome} ({jogador.personagem.nome}) em {jogador.cidade_atual.nome} ================")

    def proximo_jogador(self):
        self.id_jogador_atual = (self.id_jogador_atual + 1) % self.num_players
        self.iniciar_novo_turno()