# src/acao.py

from abc import ABC, abstractmethod
from collections import Counter
from .jogador import Jogador
from .carta import CartaCidade

class Acao(ABC):
    """ Interface para todas as ações possíveis do jogador. """
    @abstractmethod
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        """ Executa a ação e retorna True se foi bem sucedida. """
        pass

class Mover(Acao):
    """ Superclasse para todos os movimentos """
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        destino = kwargs.get('destino')
        if not destino:
            print("Erro: Cidade de destino não especificada.")
            return False
        jogador.set_cidade_atual(destino)
        return True

class MoverAutomovel(Mover):
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        destino = kwargs.get('destino')
        if destino in jogador.cidade_atual.vizinhos:
            print(f"{jogador.nome} moveu-se (Automóvel) para {destino.nome}.")
            return super().executa(jogador, **kwargs)
        else:
            print(f"Movimento inválido: {destino.nome} não é vizinha de {jogador.cidade_atual.nome}.")
            return False

class VooDireto(Mover):
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        destino = kwargs.get('destino')
        carta_voo = next((c for c in jogador.mao if isinstance(c, CartaCidade) and c.nome == destino.nome), None)
        if carta_voo:
            print(f"{jogador.nome} fez um Voo Direto para {destino.nome} descartando a carta {carta_voo.nome}.")
            jogador.descartar_carta(carta_voo)
            return super().executa(jogador, **kwargs)
        else:
            print(f"Erro: Você precisa da carta de {destino.nome} para fazer um Voo Direto.")
            return False

class VooFretado(Mover):
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        destino = kwargs.get('destino')
        carta_origem = next((c for c in jogador.mao if isinstance(c, CartaCidade) and c.nome == jogador.cidade_atual.nome), None)
        if carta_origem:
            print(f"{jogador.nome} fez um Voo Fretado para {destino.nome} descartando a carta da cidade atual ({carta_origem.nome}).")
            jogador.descartar_carta(carta_origem)
            return super().executa(jogador, **kwargs)
        else:
            print(f"Erro: Você precisa da carta de {jogador.cidade_atual.nome} para fazer um Voo Fretado.")
            return False

class PonteAerea(Mover):
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        destino = kwargs.get('destino')
        if jogador.cidade_atual.centro_pesquisa and destino.centro_pesquisa:
            print(f"{jogador.nome} usou a Ponte Aérea para ir de {jogador.cidade_atual.nome} para {destino.nome}.")
            return super().executa(jogador, **kwargs)
        else:
            print("Erro: Para usar a Ponte Aérea, ambas as cidades (origem e destino) devem ter um Centro de Pesquisa.")
            return False

class ConstruirCentro(Acao):
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        cidade = jogador.cidade_atual
        if cidade.centro_pesquisa:
            print(f"Erro: {cidade.nome} já possui um centro de pesquisa.")
            return False

        # Habilidade do Especialista em Operações
        if jogador.personagem.construir_centro_especial(jogador):
            print(f"Centro de pesquisa construído em {cidade.nome} pela habilidade do Especialista em Operações!")
            jogador.jogo.gerenciar_centros_pesquisa(cidade)
            return True

        # Regra Padrão
        carta_da_cidade = next((c for c in jogador.mao if isinstance(c, CartaCidade) and c.nome == cidade.nome), None)
        if carta_da_cidade:
            jogador.descartar_carta(carta_da_cidade)
            cidade.centro_pesquisa = True
            print(f"Centro de pesquisa construído em {cidade.nome}!")
            jogador.jogo.gerenciar_centros_pesquisa(cidade)
            return True
        else:
            print(f"Erro: Você precisa da carta de {cidade.nome} para construir um centro aqui.")
            return False

class TratarDoenca(Acao):
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        cor_doenca = kwargs.get('cor')
        if not cor_doenca:
            print("Erro: Cor da doença a ser tratada não especificada.")
            return False

        if jogador.cidade_atual.cubos[cor_doenca] == 0:
            print(f"Não há cubos da doença {cor_doenca.value} em {jogador.cidade_atual.nome}.")
            return False

        # Habilidade do Médico
        if jogador.personagem.tratar_doenca_especial(jogador.cidade_atual, cor_doenca):
            print(f"{jogador.nome} (Médico) removeu todos os cubos {cor_doenca.value} em {jogador.cidade_atual.nome}.")
            jogador.cidade_atual.remover_cubo(cor_doenca, 3, jogador.jogo) # Remove até 3
        # Regra Padrão
        else:
            # Se a cura foi descoberta, remove todos os cubos
            if jogador.jogo.doencas[cor_doenca].cura_descoberta:
                print(f"Cura descoberta! {jogador.nome} removeu todos os cubos {cor_doenca.value} em {jogador.cidade_atual.nome}.")
                jogador.cidade_atual.remover_cubo(cor_doenca, jogador.cidade_atual.cubos[cor_doenca], jogador.jogo)
            else:
                print(f"{jogador.nome} tratou a doença {cor_doenca.value} em {jogador.cidade_atual.nome}.")
                jogador.cidade_atual.remover_cubo(cor_doenca, 1, jogador.jogo)

        return True

class DesenvolverCura(Acao):
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        cor_cura = kwargs.get('cor')
        if not jogador.cidade_atual.centro_pesquisa:
            print(f"Erro: É preciso estar em um Centro de Pesquisa para descobrir a cura.")
            return False

        if jogador.jogo.doencas[cor_cura].cura_descoberta:
            print(f"A cura para a doença {cor_cura.value} já foi descoberta.")
            return False

        # Habilidade do Cientista
        cartas_necessarias = jogador.personagem.get_cartas_para_cura()

        cartas_da_cor = [c for c in jogador.mao if isinstance(c, CartaCidade) and c.cor == cor_cura]
        if len(cartas_da_cor) >= cartas_necessarias:
            jogador.jogo.doencas[cor_cura].cura_descoberta = True
            print(f"🎉 A CURA PARA A DOENÇA {cor_cura.value} FOI DESCOBERTA POR {jogador.nome}! 🎉")
            # Descarta as cartas
            for i in range(cartas_necessarias):
                jogador.descartar_carta(cartas_da_cor[i])

            # Verifica se todas as curas foram descobertas (condição de vitória)
            if all(d.cura_descoberta for d in jogador.jogo.doencas.values()):
                jogador.jogo.fim_de_jogo("vitoria", "Todas as quatro doenças foram curadas!")
            return True
        else:
            print(f"Não há cartas suficientes ({len(cartas_da_cor)}/{cartas_necessarias}) para descobrir a cura da doença {cor_cura.value}.")
            return False

class Compartilhar(Acao):
    def executa(self, jogador: Jogador, **kwargs) -> bool:
        outro_jogador = kwargs.get('outro_jogador')
        carta = kwargs.get('carta') # A carta a ser trocada
        acao_tipo = kwargs.get('tipo') # "dar" ou "pegar"

        if not outro_jogador or not carta or not acao_tipo:
            print("Argumentos inválidos para compartilhar.")
            return False
        if jogador.cidade_atual != outro_jogador.cidade_atual:
            print("Jogadores precisam estar na mesma cidade para compartilhar cartas.")
            return False

        # Habilidade da Pesquisadora (modifica a regra de DAR)
        if acao_tipo == "dar" and jogador.personagem.compartilhar_conhecimento_especial(jogador, outro_jogador, carta):
             if carta in jogador.mao:
                jogador.mao.remove(carta) # Remove sem descartar
                outro_jogador.adicionar_carta_mao(carta)
                print(f"{jogador.nome} (Pesquisadora) deu a carta '{carta.nome}' para {outro_jogador.nome}.")
                return True
             else:
                return False

        # Regra Padrão: a carta deve ser da cidade atual
        if carta.nome != jogador.cidade_atual.nome:
            print(f"Erro: A troca de cartas só pode ser da cidade em que os jogadores estão ({jogador.cidade_atual.nome}).")
            return False

        if acao_tipo == "dar":
            if carta in jogador.mao:
                jogador.mao.remove(carta)
                outro_jogador.adicionar_carta_mao(carta)
                print(f"{jogador.nome} deu a carta '{carta.nome}' para {outro_jogador.nome}.")
                return True
        elif acao_tipo == "pegar":
            if carta in outro_jogador.mao:
                outro_jogador.mao.remove(carta)
                jogador.adicionar_carta_mao(carta)
                print(f"{jogador.nome} pegou a carta '{carta.nome}' de {outro_jogador.nome}.")
                return True
        return False