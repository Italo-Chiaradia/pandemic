# src/doenca.py

from enum import Enum

class Cor(Enum):
    AZUL = "Azul"
    AMARELO = "Amarelo"
    PRETO = "Preto"
    VERMELHO = "Vermelho"

class Doenca:
    def __init__(self, cor: Cor):
        self.cor = cor
        self.erradicada = False
        self.cura_descoberta = False
        # NOVO: Contador de cubos disponíveis
        self.cubos_disponiveis = 24

    def __repr__(self):
        status = "Errada" if self.erradicada else "Curada" if self.cura_descoberta else "Ativa"
        return f"Doenca({self.cor.value}, Status: {status}, Cubos: {self.cubos_disponiveis})"