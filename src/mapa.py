# src/mapa.py

from .cidade import Cidade

class Mapa:
    """ Mantém o registro de todas as cidades do jogo. """
    def __init__(self):
        self.cidades = {}  # Dicionário para acesso rápido pelo nome

    def adicionar_cidade(self, cidade: Cidade):
        """ Adiciona uma cidade ao mapa. """
        self.cidades[cidade.nome] = cidade

    def get_cidade(self, nome: str) -> Cidade | None:
        """ Retorna uma instância de cidade a partir de seu nome. """
        return self.cidades.get(nome)

    def __repr__(self):
        return f"Mapa com {len(self.cidades)} cidades."