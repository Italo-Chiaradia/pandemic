# src/carta.py

from abc import ABC
from .doenca import Cor
# NOVO: Importa a classe base Personagem
from .personagem import Personagem

class Carta(ABC):
    def __init__(self, nome: str):
        self.nome = nome

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.nome}')"

class CartaCidade(Carta):
    def __init__(self, nome: str, cor: Cor, populacao: int): # NOVO: Adiciona população
        super().__init__(nome)
        self.cor = cor
        self.populacao = populacao # NOVO

class CartaEvento(Carta):
    def __init__(self, nome: str, descricao: str):
        super().__init__(nome)
        self.descricao = descricao

class CartaEpidemia(Carta):
    def __init__(self):
        super().__init__("Epidemia")

# MODIFICADO: Esta classe não é mais necessária, pois usaremos as instâncias de Personagem
# class CartaPersonagem(Carta):
#     def __init__(self, nome: str, habilidade: str):
#         super().__init__(nome)
#         self.habilidade = habilidade

class CartaInfeccao(CartaCidade): # MODIFICADO: Nome mais claro
    pass