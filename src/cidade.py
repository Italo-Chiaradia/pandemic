# src/cidade.py
from __future__ import annotations
from typing import TYPE_CHECKING, Set, Dict
from .doenca import Cor
from .personagem import Medico, EspecialistaQuarentena

if TYPE_CHECKING:
    from .jogo import Jogo

class Cidade:
    def __init__(self, nome: str, cor: Cor, populacao: int):
        self.nome = nome
        self.cor = cor
        self.populacao = populacao
        self.cubos: Dict[Cor, int] = {c: 0 for c in Cor}
        self.vizinhos: Set[Cidade] = set()
        self.centro_pesquisa = False

    def adicionar_vizinho(self, vizinho: 'Cidade'):
        if vizinho not in self.vizinhos:
            self.vizinhos.add(vizinho)
            vizinho.vizinhos.add(self)

    # MODIFICADO: A assinatura agora aceita o conjunto de cidades que já surtaram
    def adicionar_cubo(self, cor: Cor, jogo: 'Jogo', cidades_ja_surtaram: set):
        # Habilidade do Especialista em Quarentena
        for jogador in jogo.jogadores:
            if isinstance(jogador.personagem, EspecialistaQuarentena):
                if self == jogador.cidade_atual or self in jogador.cidade_atual.vizinhos:
                    print(f"Infecção em {self.nome} prevenida pelo Especialista em Quarentena.")
                    return
        
        # Habilidade do Médico
        for jogador in jogo.jogadores:
            if jogador.cidade_atual == self and isinstance(jogador.personagem, Medico) and jogo.doencas[cor].cura_descoberta:
                print(f"Médico preveniu a infecção em {self.nome}.")
                return

        if self.cubos[cor] < 3:
            if jogo.doencas[cor].cubos_disponiveis > 0:
                self.cubos[cor] += 1
                jogo.doencas[cor].cubos_disponiveis -= 1
                print(f"Cubo {cor.value} adicionado em {self.nome}. Total: {self.cubos[cor]}")
            else:
                jogo.fim_de_jogo("derrota_cubos", f"Acabaram os cubos da doença {cor.value}!")
        else:
            # Passa o conjunto de cidades já surtadas para a lógica de surto
            jogo.surto(self, cor, cidades_ja_surtaram)

    def remover_cubo(self, cor: Cor, quantidade: int, jogo: 'Jogo'):
        removidos = min(quantidade, self.cubos[cor])
        self.cubos[cor] -= removidos
        jogo.doencas[cor].cubos_disponiveis += removidos
        print(f"{removidos} cubo(s) {cor.value} removido(s) de {self.nome}. Restantes: {self.cubos[cor]}")
        
        if jogo.doencas[cor].cura_descoberta:
            total_cubos_no_mapa = sum(c.cubos[cor] for c in jogo.mapa.cidades.values())
            if total_cubos_no_mapa == 0:
                jogo.doencas[cor].erradicada = True
                print(f"DOENÇA {cor.value} FOI ERRADICADA!")

    def __repr__(self):
        return f"Cidade('{self.nome}', Cor.{self.cor.name})"