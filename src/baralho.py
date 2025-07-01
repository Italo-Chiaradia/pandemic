# src/baralho.py

import random
from .carta import Carta

class Baralho:
    def __init__(self, tipo: str, cartas: list[Carta]):
        self.tipo = tipo
        self.cartas_compra = cartas
        self.cartas_descarte = []
        self.embaralhar()

    def embaralhar(self):
        random.shuffle(self.cartas_compra)

    def comprar(self) -> Carta | None:
        if len(self.cartas_compra) > 0:
            return self.cartas_compra.pop(0)
        return None

    # NOVO: Compra a carta de BAIXO do baralho (para Epidemia)
    def comprar_de_baixo(self) -> Carta | None:
        if len(self.cartas_compra) > 0:
            return self.cartas_compra.pop()
        return None

    def descartar(self, carta: Carta):
        self.cartas_descarte.append(carta)

    # NOVO: Embaralha o descarte e coloca no topo (para Epidemia)
    def intensificar(self):
        print("Intensificando o baralho de infecção...")
        random.shuffle(self.cartas_descarte)
        self.cartas_compra = self.cartas_descarte + self.cartas_compra
        self.cartas_descarte = []

    def __len__(self):
        return len(self.cartas_compra)