import numpy as np
import random
import math

# parâmetros do drone
G = 9.81              # gravidade
ne = 0.66             # eficiência de transferência de energia
r = 3.5               # razão do arrasto
Fsb = 1.25            # fator de segurança da bateria
ma = 10.1             # massa do drone + bateria (kg)
B = 2_797_200         # energia total da bateria (J)

# cálculo do consumo de bateria bij
def calc_bij(wi, dij):
  return dij * (2 * ma + wi) * Fsb * G / (ne * r)

def abrir_facilidades(n, m, p, wi, dij, t=10):
  bij = np.zeros((n, m))
  wtij = np.zeros((n, m))

  for i in range(n):
    for j in range(m):
      bij[i][j] = calc_bij(wi[i], dij[i][j])
      wtij[i][j] = wi[i] / bij[i][j] if bij[i][j] <= B else 0

  # lista ordenada L dos pesos (i, j, wtij)
  L = sorted(
    [(i, j, wtij[i][j]) for i in range(n) for j in range(m) if wtij[i][j] > 0],
    key=lambda x: x[2],
    reverse=True,
  )

  Jopen = set()
  L_copy = L.copy()

  while len(Jopen) < p and L:
    top_t = L[:t] if len(L) >= t else L
    _, j_selected, _ = random.choice(top_t)

    if j_selected not in Jopen:
      Jopen.add(j_selected)
      L = [entry for entry in L if entry[1] != j_selected] # evita repetição

  return list(Jopen), L_copy

def alocar_clientes(Jopen, L_copy, wi, capacidade_U):
  capacidade = {j: capacidade_U for j in Jopen}
  clientes_atendidos = set()
  C = []

  for i, j, wt in L_copy:
    if i in clientes_atendidos:
      continue

    if j in capacidade and capacidade[j] >= wi[i]:
      C.append((i, j))
      capacidade[j] -= wi[i]
      clientes_atendidos.add(i)

  return C

def alocar_drones(Jopen, C, bij, B, nd):
  drones_por_facilidade = {j: 0 for j in Jopen}
  total_drones_necessarios = 0

  for j in Jopen:
    soma = sum(bij[i][j] for (i, jj) in C if jj == j)
    drones_necessarios = math.ceil(soma / B)
    drones_por_facilidade[j] = drones_necessarios
    total_drones_necessarios += drones_necessarios

  # atribuição sequencial até acabar os drones
  Jorder = sorted(drones_por_facilidade.items(), key=lambda x: x[1], reverse=True)
  atribuicao = {j: 0 for j in Jopen}
  total_atribuido = 0

  while total_atribuido < min(nd, total_drones_necessarios):
    for j, limite in Jorder:
      if atribuicao[j] < limite:
        atribuicao[j] += 1
        total_atribuido += 1

        if total_atribuido >= nd:
          break

  return atribuicao

def atender_clientes(Jopen, C, bij, B, drones_por_facilidade):
  atendimento = {j: [] for j in Jopen}
  clientes_por_j = {j: [] for j in Jopen}

  for i, j in C:
    clientes_por_j[j].append((i, bij[i][j]))

  for j in Jopen:
    clientes_ordenados = sorted(clientes_por_j[j], key=lambda x: x[1])
    drones = [[] for _ in range(drones_por_facilidade[j])]
    baterias = [B] * drones_por_facilidade[j]

    for i, b in clientes_ordenados:
      alocado = False

      for d in range(len(drones)):
        if baterias[d] >= b:
          drones[d].append(i)
          baterias[d] -= b
          alocado = True
          break

      if not alocado:
        continue # não foi possível atender esse cliente

      atendimento[j] = drones

  return atendimento

def calcular_funcao_objetivo(wi, atendimento):
  clientes_atendidos = set()

  for drones in atendimento.values():
    for drone in drones:
      for cliente in drone:
        clientes_atendidos.add(cliente)

  demanda_total_atendida = sum(wi[i] for i in clientes_atendidos)
  demanda_total = sum(wi)

  return demanda_total_atendida / demanda_total
