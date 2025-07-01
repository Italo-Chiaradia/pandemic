# src/gui/config.py

import pygame
import os # NOVO: Importa o módulo 'os' para lidar com caminhos de arquivo
from src.doenca import Cor

# --- NOVO: Lógica para criar um caminho absoluto para os assets ---
# Pega o diretório do arquivo atual (config.py)
# Ex: C:/.../pandemic-game-main/src/gui
base_dir = os.path.dirname(os.path.abspath(__file__))
# Volta dois níveis para chegar na raiz do projeto (pandemic-game-main)
# de 'src/gui' para 'src' -> para 'pandemic-game-main'
project_root = os.path.dirname(os.path.dirname(base_dir))
# Cria o caminho completo para a pasta de assets
assets_path = os.path.join(project_root, 'assets')
# -------------------------------------------------------------


# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (200, 200, 200)
VERDE_CLARO = (144, 238, 144)
AMARELO_CLARO = (255, 255, 224)
VERMELHO = (220, 20, 60)
AZUL = (0, 121, 189),

COR_DOENCA = {
    Cor.AZUL: (0, 121, 189),
    Cor.AMARELO: (252, 220, 0),
    Cor.PRETO: (70, 70, 70),
    Cor.VERMELHO: (220, 20, 60)
}
COR_CURA_DESCOBERTA = (150, 255, 150)
COR_ERRADICADA = (255, 165, 0)
COR_PEAO_JOGADOR = [(255, 105, 180), (135, 206, 250), (255, 215, 0), (218, 112, 214)]

# Tela
LARGURA_TELA = 1280
ALTURA_TELA = 800
FPS = 60

# Fontes
pygame.font.init()
FONTE_PADRAO = pygame.font.Font(None, 24)
FONTE_CIDADE = pygame.font.Font(None, 18)
FONTE_TITULO = pygame.font.Font(None, 36)
FONTE_INFO = pygame.font.Font(None, 20)
FONTE_CARTA = pygame.font.Font(None, 16)


# Mapa
# MODIFICADO: Usa o caminho absoluto que criamos
CAMINHO_IMAGEM_MAPA = os.path.join(assets_path, 'mapa_mundi.png')

# Coordenadas das cidades (sem alteração)
COORDENADAS_CIDADES = {
    "São Francisco": (125, 205), "Chicago": (210, 180), "Atlanta": (250, 240),
    "Montreal": (290, 170), "Nova Iorque": (340, 200), "Washington": (320, 250),
    "Londres": (480, 160), "Madri": (470, 225), "Paris": (540, 190),
    "Milão": (590, 170), "Essen": (560, 130), "São Petersburgo": (660, 135),
    
    "Los Angeles": (160, 280), "Cidade do México": (210, 320), "Miami": (290, 300),
    "Bogotá": (290, 380), "Lima": (260, 450), "Santiago": (250, 540),
    "Buenos Aires": (340, 530), "São Paulo": (400, 480), "Lagos": (510, 390),
    "Kinshasa": (580, 430), "Joanesburgo": (620, 520), "Khartoum": (640, 380),
    
    "Argel": (540, 280), "Cairo": (620, 290), "Istambul": (630, 210),
    "Moscou": (700, 190), "Bagdá": (700, 270), "Riad": (710, 330),
    "Teerã": (760, 220), "Karachi": (790, 280), "Mumbai": (820, 340),
    "Deli": (840, 260), "Calcutá": (910, 290), "Chenai": (860, 400),
    
    "Pequim": (950, 180), "Seul": (1020, 180), "Xangai": (960, 240),
    "Tóquio": (1080, 210), "Osaka": (1090, 260), "Taipé": (1020, 310),
    "Hong Kong": (970, 320), "Manila": (1060, 400), "Bangkok": (930, 360),
    "Cidade de Ho Chi Minh": (980, 410), "Jacarta": (940, 480), "Sydney": (1120, 560)
}