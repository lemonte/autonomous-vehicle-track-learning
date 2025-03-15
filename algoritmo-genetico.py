import numpy as np
# import streamlit as st
import time
from random import choice, randint, random

# Ícones
CAR_ICON = '🚗'
BURNED_CAR_ICON = '💥'
ROAD_ICON = '⬜'
WALL_ICON = '⬛'
FINISH_ICON = '🏁'
PATH_ICON = '🟩'



final_pos = (1, 5)
initial_pos = (16, 5)
# Configuração da pista
pista = np.full((20, 20), 1)

# Destino final


def pista2():
    global initial_pos, final_pos
    for r in range(4, 7):
        for c in range(9, 12):
            pista[r, c] = 0
            
    for r in range(10, 13):
        for c in range(9, 12):
            pista[r, c] = 0

    for r in range(10, 13):
        for c in range(6, 9):
            pista[r, c] = 0

    for r in range(10, 18):
        for c in range(3, 6):
            pista[r, c] = 0

    for r in range(4, 7):
        for c in range(4, 12):
            pista[r, c] = 0

    for r in range(1, 4):
        for c in range(4, 7):
            pista[r, c] = 0


    for r in range(7, 10):
        for c in range(9, 12):
            pista[r, c] = 0

    final_pos = (1, 5)
    initial_pos = (16, 5)



def pista1():
    global initial_pos, final_pos
    for r in range(4, 7):
        for c in range(9, 12):
            pista[r, c] = 0

    # Encruzilhada ESQUERDA
    for r in range(10, 13):
        for c in range(9, 12):
            pista[r, c] = 0

    for r in range(10, 13):
        for c in range(6, 9):
            pista[r, c] = 0

    for r in range(10, 18):
        for c in range(3, 6):
            pista[r, c] = 0

    for r in range(4, 7):
        for c in range(12, 15):
            pista[r, c] = 0

    for r in range(1, 4):
        for c in range(12, 15):
            pista[r, c] = 0


    for r in range(7, 10):
        for c in range(9, 12):
            pista[r, c] = 0

    final_pos = (1, 14)
    initial_pos = (16, 5)


pista2()

direcoes = ['up', 'left', 'down', 'right']

class Carro:
    def __init__(self, pista, genes=None):
        self.pista = pista
        self.posicao = initial_pos
        self.queimado = False
        self.pontos = 0
        # self.genes = genes if genes else [choice(direcoes) for _ in range(100)]
        self.passo = 0
        self.caminho = [initial_pos]
        self.situacoes = {}
        self.genes = genes if genes else {}

    def mover(self):
        if self.queimado:
            return
        if self.passo >= 40 or (self.posicao[0] == final_pos[0] and self.posicao[1] == final_pos[1]):
            self.queimado = True
            return
        # if self.queimado or self.passo >= len(self.genes):
        #     return

        # direcao = self.genes[self.passo]
        direcao = self.decidir_movimento()
        self.passo += 1

        x, y = self.posicao
        novo_x, novo_y = x, y

        if direcao == 'up': novo_x -= 1
        elif direcao == 'down': novo_x += 1
        elif direcao == 'left': novo_y -= 1
        elif direcao == 'right': novo_y += 1

        if (0 <= novo_x < self.pista.shape[0] and
            0 <= novo_y < self.pista.shape[1] and
            self.pista[novo_x, novo_y] == 0):
            self.posicao = [novo_x, novo_y]
            self.pontos += 1
            self.caminho.append((novo_x, novo_y))
        else:
            self.queimado = True

    def fitness(self):
        dist = np.linalg.norm(np.array(self.posicao) - np.array(final_pos))
        bonus = 1000 if self.posicao == list(final_pos) else 0
        return 1 / (dist + 1 + (self.passo * 0.2)) + initial_pos[0] - self.posicao[0] + bonus

    def decidir_movimento(self):
        situacao = self.sensores()
        if situacao not in self.genes:
            self.genes[situacao] = choice(direcoes)
        return self.genes[situacao]

    def sensores(self):
        x, y = self.posicao
        distancias = []

        # Esquina superior esquerda
        dist_sup_esq = 0
        i, j = x-1, y-1
        while i >= 0 and j >= 0:
            if self.pista[i, j] == 1:
                break
            dist_sup_esq += 1
            i -= 1
            j -= 1
        distancias.append(dist_sup_esq)

        # Cima
        dist_cima = 0
        for i in range(x-1, -1, -1):
            if self.pista[i, y] == 1:
                break
            dist_cima += 1
        distancias.append(dist_cima)

        # Esquina superior direita
        dist_sup_dir = 0
        i, j = x-1, y+1
        while i >= 0 and j < self.pista.shape[1]:
            if self.pista[i, j] == 1:
                break
            dist_sup_dir += 1
            i -= 1
            j += 1
        distancias.append(dist_sup_dir)

        # Esquerda
        dist_esquerda = 0
        for j in range(y-1, -1, -1):
            if self.pista[x, j] == 1:
                break
            dist_esquerda += 1
        distancias.append(dist_esquerda)

        # Direita
        dist_direita = 0
        for j in range(y+1, self.pista.shape[1]):
            if self.pista[x, j] == 1:
                break
            dist_direita += 1
        distancias.append(dist_direita)

        # Esquina inferior esquerda
        dist_inf_esq = 0
        i, j = x+1, y-1
        while i < self.pista.shape[0] and j >= 0:
            if self.pista[i, j] == 1:
                break
            dist_inf_esq += 1
            i += 1
            j -= 1
        distancias.append(dist_inf_esq)

        # Baixo
        dist_baixo = 0
        for i in range(x+1, self.pista.shape[0]):
            if self.pista[i, y] == 1:
                break
            dist_baixo += 1
        distancias.append(dist_baixo)

        # Esquina inferior direita
        dist_inf_dir = 0
        i, j = x+1, y+1
        while i < self.pista.shape[0] and j < self.pista.shape[1]:
            if self.pista[i, j] == 1:
                break
            dist_inf_dir += 1
            i += 1
            j += 1
        distancias.append(dist_inf_dir)

        return tuple(distancias)

def torneio(carros, tamanho_torneio=3):
    competidores = [choice(carros) for _ in range(tamanho_torneio)]
    return max(competidores, key=lambda c: c.fitness())

# Funções genéticas
def crossover(pai, mae):
    filho_genes = {}
    todas_situacoes = set(pai.genes.keys()).union(mae.genes.keys())
    for situacao in todas_situacoes:
        if situacao in pai.genes and situacao in mae.genes:
            filho_genes[situacao] = choice([pai.genes[situacao], mae.genes[situacao]])
        else:
            filho_genes[situacao] = choice(direcoes)
    return Carro(pista, filho_genes)


def mutacao(carro, taxa=0.15):
    # for i in range(len(carro.genes)):
    for situacao in carro.genes:
        if random() < taxa:
            # carro.genes[i] = choice(direcoes)
            carro.genes[situacao] = choice(direcoes)

def mostrar_melhor_percurso(pista, carro):
    percurso = carro.caminho
    display = ''
    for i in range(pista.shape[0]):
        linha = ''
        for j in range(pista.shape[1]):
            if (i, j) in percurso:
                linha += PATH_ICON
            elif (i, j) == final_pos:
                linha += FINISH_ICON
            elif pista[i, j] == 1:
                linha += WALL_ICON
            else:
                linha += ROAD_ICON
        display += linha + '\n'
    return display

# Exibição
def mostrar_pista(pista, carros):
    display = ''
    for i in range(pista.shape[0]):
        linha = ''
        for j in range(pista.shape[1]):
            carro_aqui = next((c for c in carros if c.posicao == [i, j]), None)
            if carro_aqui:
                linha += str(int(carro_aqui.fitness()*100)) if carro_aqui.queimado else CAR_ICON
            elif (i, j) == final_pos:
                linha += FINISH_ICON
            elif pista[i, j] == 1:
                linha += WALL_ICON
            else:
                linha += ROAD_ICON
        display += linha + '\n'
    return display

# st.title("🏁 Simulador de Corrida com Algoritmo Genético 🏁")

# População inicial
populacao = 100
carros = [Carro(pista) for _ in range(populacao)]
geracao = 1
# placeholder = st.empty()

ultimo_fitness = None
contador_estagnacao = 0
contador_melhor_fitness = 0

while True:
    print(f"Geração: {geracao}")
    todos_parados = False

    while not todos_parados:
        todos_parados = True
        for carro in carros:
            if not carro.queimado:
                carro.mover()
                todos_parados = False

        result_pista = mostrar_pista(pista, carros)
        print(result_pista)
        # placeholder.markdown(result_pista)
        time.sleep(0.01)

        # if any(tuple(c.posicao) == final_pos for c in carros):
            # vencedor = max(carros, key=lambda c: c.fitness())
            # print(f"🏆 Um carro chegou ao final com fitness: {vencedor.fitness():.2f}!")
            # print(vencedor.genes)
            # print(mostrar_melhor_percurso(pista, vencedor))
            # st.markdown(mostrar_melhor_percurso(pista, vencedor))
            # break

    carros.sort(key=lambda c: c.fitness(), reverse=True)

    melhor_fitness_atual = carros[0].fitness()
    if ultimo_fitness is not None and abs(ultimo_fitness - melhor_fitness_atual) < 0.001:
        contador_estagnacao += 1
    else:
        contador_estagnacao = 0
    ultimo_fitness = melhor_fitness_atual

    if contador_estagnacao > 20:
        # st.warning("O algoritmo convergiu para um ótimo local!")
        vencedor = carros[0]
        print(f" Geracao: {geracao}")
        print(f"🏆 Um carro chegou ao final com fitness: {vencedor.fitness():.2f}!")
        print(vencedor.genes)
        print(mostrar_melhor_percurso(pista, vencedor))
        # st.markdown(mostrar_melhor_percurso(pista, vencedor))
        break

    elite_size = max(1, int(populacao * 0.1))
    elite = carros[:elite_size]

    nova_geracao = elite.copy()

    while len(nova_geracao) < populacao:
        pai = torneio(carros)
        mae = torneio(carros)
        filho = crossover(pai, mae)
        mutacao(filho, taxa=0.15)
        nova_geracao.append(filho)

    carros = nova_geracao
    geracao += 1
