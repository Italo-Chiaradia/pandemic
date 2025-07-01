# src/turno.py

from .jogador import Jogador
from .acao import Acao
from .carta import CartaEpidemia

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .jogo import Jogo

class Turno:
    def __init__(self, jogador_atual: Jogador, jogo: 'Jogo'):
        self.jogador_atual = jogador_atual
        self.jogo = jogo
        self.acoes_restantes = 4

    def realizar_acao(self, acao: Acao, **kwargs) -> bool:
        if self.acoes_restantes > 0:
            print(f"\n--- Ação de {self.jogador_atual.nome} ---")
            sucesso = acao.executa(self.jogador_atual, **kwargs)
            if sucesso:
                self.acoes_restantes -= 1
                print(f"Ações restantes: {self.acoes_restantes}")
                return True
            else:
                print("Ação falhou.")
                return False
        else:
            print("Não há mais ações disponíveis neste turno.")
            return False

    def finalizar_fase_acoes(self):
        print("\n--- Fim da Fase de Ações ---")
        self._comprar_cartas_jogador()
        if self.jogo.game_over: return

        print("\n--- Fase de Infecção ---")
        self._infectar_cidades()
        if self.jogo.game_over: return

        self.jogo.proximo_jogador()

    def _comprar_cartas_jogador(self):
        print("Comprando 2 cartas de jogador...")
        for _ in range(2):
            if self.jogo.game_over: break

            carta = self.jogo.baralho_jogador.comprar()
            if carta:
                if isinstance(carta, CartaEpidemia):
                    print("🚨 EPIDEMIA! 🚨")
                    self.jogo.epidemia()
                else:
                    self.jogador_atual.adicionar_carta_mao(carta)
                    print(f"{self.jogador_atual.nome} comprou a carta {carta.nome}.")
            else:
                self.jogo.fim_de_jogo("derrota_cartas", "Acabaram as cartas de jogador!")
                return

    def _infectar_cidades(self):
        taxa_infeccao = self.jogo.get_taxa_infeccao()
        print(f"Taxa de Infecção: {taxa_infeccao}. Revelando {taxa_infeccao} carta(s)...")
        for _ in range(taxa_infeccao):
            if self.jogo.game_over: break

            carta_infeccao = self.jogo.baralho_infeccao.comprar()
            if carta_infeccao:
                cidade_obj = self.jogo.mapa.get_cidade(carta_infeccao.nome)
                if self.jogo.doencas[cidade_obj.cor].erradicada:
                    print(f"Infecção em {cidade_obj.nome} ignorada (doença erradicada).")
                else:
                    print(f"Infectando {cidade_obj.nome}...")
                    # MODIFICADO: A chamada agora passa um novo conjunto vazio para iniciar a cadeia.
                    cidade_obj.adicionar_cubo(cidade_obj.cor, self.jogo, set())

                self.jogo.baralho_infeccao.descartar(carta_infeccao)