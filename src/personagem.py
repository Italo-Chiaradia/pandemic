# src/personagem.py

from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .cidade import Cidade
    from .jogador import Jogador
    from .carta import CartaCidade

class Personagem:
    """ Classe base para todos os personagens. """
    def __init__(self, nome: str, habilidade: str):
        self.nome = nome
        self.habilidade = habilidade

    def get_cartas_para_cura(self) -> int:
        return 5

    def tratar_doenca_especial(self, cidade: Cidade, cor: str) -> bool:
        return False

    def construir_centro_especial(self, jogador: Jogador) -> bool:
        return False

    def compartilhar_conhecimento_especial(self, jogador_da_vez: Jogador, outro_jogador: Jogador, carta: CartaCidade) -> bool:
        return False

class Cientista(Personagem):
    def __init__(self):
        super().__init__("Cientista", "Precisa de apenas 4 cartas para descobrir a cura.")

    def get_cartas_para_cura(self) -> int:
        return 4

class Medico(Personagem):
    def __init__(self):
        super().__init__("Médico", "Remove todos os cubos de uma cor ao Tratar.")

    def tratar_doenca_especial(self, cidade: Cidade, cor: str) -> bool:
        if cidade.cubos[cor] > 0:
            removidos = cidade.cubos[cor]
            cidade.cubos[cor] = 0
            # A lógica de devolver os cubos para o estoque está em remover_cubo
            return True
        return False

class Pesquisadora(Personagem):
    def __init__(self):
        super().__init__("Pesquisadora", "Pode dar qualquer carta de cidade a um jogador na mesma cidade.")

    def compartilhar_conhecimento_especial(self, jogador_da_vez: Jogador, outro_jogador: Jogador, carta: CartaCidade) -> bool:
        if jogador_da_vez.personagem.nome == self.nome:
            if carta in jogador_da_vez.mao:
                return True
        return False

class EspecialistaOperacoes(Personagem):
    def __init__(self):
        super().__init__("Especialista em Operações", "Pode construir um Centro de Pesquisa em sua cidade sem a carta.")

    def construir_centro_especial(self, jogador: Jogador) -> bool:
        cidade = jogador.cidade_atual
        if not cidade.centro_pesquisa:
            cidade.centro_pesquisa = True
            jogador.jogo.gerenciar_centros_pesquisa(cidade)
            return True
        return False

# --- NOVO PERSONAGEM ADICIONADO AQUI ---
class EspecialistaQuarentena(Personagem):
    def __init__(self):
        super().__init__("Especialista em Quarentena", "Previne surtos e infecções na sua cidade e cidades vizinhas.")
        # A habilidade deste personagem é passiva e verificada nos métodos de infecção/surto.