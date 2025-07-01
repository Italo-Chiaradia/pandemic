# src/jogador.py
from __future__ import annotations
from typing import List, TYPE_CHECKING
from .carta import Carta
from .personagem import Personagem

if TYPE_CHECKING:
    from .cidade import Cidade
    from .jogo import Jogo


class Jogador:
    def __init__(self, nome: str, personagem: Personagem, jogo: 'Jogo'):
        self.nome = nome
        self.personagem = personagem
        self.mao: List[Carta] = []
        self.cidade_atual: Cidade | None = None
        # NOVO: Referência ao jogo para checagem de regras
        self.jogo = jogo
        self.limite_mao = 7

    def set_cidade_atual(self, cidade: Cidade):
        self.cidade_atual = cidade
        # NOVO: Habilidade passiva do médico
        if hasattr(self.personagem, 'on_enter_city'):
            self.personagem.on_enter_city(cidade, self.jogo.doencas)

    def adicionar_carta_mao(self, carta: Carta):
        self.mao.append(carta)
        self.verificar_limite_mao()

    def descartar_carta(self, carta: Carta) -> Carta | None:
        if carta in self.mao:
            self.mao.remove(carta)
            self.jogo.baralho_jogador.descartar(carta)
            return carta
        return None

    # NOVO: Lógica para forçar o descarte se a mão exceder o limite
    def verificar_limite_mao(self):
        while len(self.mao) > self.limite_mao:
            print(f"ALERTA: {self.nome} tem {len(self.mao)} cartas! Precisa descartar {len(self.mao) - self.limite_mao}.")
            # Em um jogo real, aqui entraria a interface para o jogador escolher o que descartar.
            # Por simplicidade, vamos descartar a primeira carta.
            carta_a_descartar = self.mao[0]
            self.descartar_carta(carta_a_descartar)
            print(f"{self.nome} descartou {carta_a_descartar.nome} para respeitar o limite de mão.")


    def __repr__(self):
        return f"Jogador('{self.nome}', Personagem: {self.personagem.nome})"