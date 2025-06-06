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
 
def open_facilities(n, m, p, wi, dij, t=10):
  bij = np.zeros((n, m)) # matriz de consumo de bateria
  wtij = np.zeros((n, m)) # matriz de pesos demanda x consumo

  for i in range(n):
    for j in range(m):
      bij[i][j] = calc_bij(wi[i], dij[i][j])
      wtij[i][j] = wi[i] / bij[i][j] if bij[i][j] <= B else 0 # quanto maior a demanda e menor o consumo, melhor o peso

  # lista ordenada L dos pesos (i, j, wtij)
  L = sorted(
    [(i, j, wtij[i][j]) for i in range(n) for j in range(m) if wtij[i][j] > 0],
    key=lambda x: x[2],
    reverse=True,
  )

  Jopen = set()
  L1 = L.copy()

  while len(Jopen) < p and L:
    top_t = L[:t] if len(L) >= t else L
    _, j_selected, _ = random.choice(top_t)

    if j_selected not in Jopen:
      Jopen.add(j_selected)
      L = [entry for entry in L if entry[1] != j_selected] # evita repetição

  return list(Jopen), L1

def allocate_clients(Jopen, L1, wi, U):
  capacity = {j: U for j in Jopen}
  clients_served = set()
  C = []

  for (i, j, wt) in L1:
    if i in clients_served:
      continue

    if j in capacity and capacity[j] >= wi[i]:
      C.append((i, j))
      capacity[j] -= wi[i]
      clients_served.add(i)

  return C

def allocate_drones(nd, Jopen, C, bij):
  drones_by_facility = {j: 0 for j in Jopen}
  total_necessary_drones = 0

  for j in Jopen:
    battery_sum = sum(bij[i][j] for (i, jj) in C if jj == j)
    necessary_drones = math.ceil(battery_sum / B)
    drones_by_facility[j] = necessary_drones
    total_necessary_drones += necessary_drones

  # atribuição sequencial até acabar os drones
  Jorder = sorted(drones_by_facility.items(), key=lambda x: x[1], reverse=True)
  allocation = {j: 0 for j in Jopen}
  total_allocated = 0

  while total_allocated < min(nd, total_necessary_drones):
    for j, limit in Jorder:
      if allocation[j] < limit:
        allocation[j] += 1
        total_allocated += 1

        if total_allocated >= nd:
          break

  return allocation

def serve_clients(Jopen, C, bij, drones_by_facility):
  service = {j: [] for j in Jopen} # atendimento
  clients_by_facility = {j: [] for j in Jopen}

  for i, j in C:
    clients_by_facility[j].append((i, bij[i][j]))

  for j in Jopen:
    sorted_clients = sorted(clients_by_facility[j], key=lambda x: x[1])
    drones = [[] for _ in range(drones_by_facility[j])]
    batteries = [B] * drones_by_facility[j]

    for i, b in sorted_clients:
      allocated = False

      for d in range(len(drones)):
        if batteries[d] >= b:
          drones[d].append(i)
          batteries[d] -= b
          allocated = True
          break

      if not allocated:
        continue # não foi possível atender esse cliente

      service[j] = drones

  return service

def calc_target_function(wi, service):
  clients_served = set()

  for drones in service.values():
    for drone in drones:
      for client in drone:
        clients_served.add(client)

  total_demand_served = sum(wi[i] for i in clients_served)
  total_demand = sum(wi)

  return total_demand_served / total_demand
