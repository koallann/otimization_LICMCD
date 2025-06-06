from math import cos, radians, sqrt
import time

from dataset import *
from heuristic import *
from genetic_algorithm import *

def build_demands(demands):
  return [d["Demand (kg)"] for d in demands]

def build_distances(demands, facility_candidates):

  def calc_distance(lat1, lon1, lat2, lon2):
    lat1_rad, lat2_rad = radians(lat1), radians(lat2)
    lat_media = (lat1_rad + lat2_rad) / 2
    dx = 111320 * cos(lat_media) * (lon2 - lon1)
    dy = 111320 * (lat2 - lat1)
    return sqrt(dx**2 + dy**2)

  dij = []

  for d in demands:
    row = []

    for c in facility_candidates:
      dist = calc_distance(d["Latitude"], d["Longitude"], c["Latitude"], c["Longitude"])
      row.append(dist)

    dij.append(row)

  return dij

# construindo lista de demandas (clientes) e mapa de distâncias (de demanda p/ instalação) 
wi = build_demands(clients)
dij = build_distances(clients, facility_candidates)

n = len(wi) # total de demandas
m = len(facility_candidates) # total de candidatos à instalação (centro de distribuição)
p = 15 # parâmetro: quantidade de instalações
nd = 60 # parâmetro: quantidade de drones
U = sum(wi) / (0.8 * p) # capacidade de cada instalação

# Jopen, L1 = open_facilities(n, m, p, wi, dij)
# C = allocate_clients(Jopen, L1, wi, U)
# bij = np.array([[calc_bij(wi[i], dij[i][j]) for j in range(m)] for i in range(n)])
# allocation = allocate_drones(nd, Jopen, C, bij)
# service = serve_clients(Jopen, C, bij, allocation)

# print("Facilidades abertas:", Jopen)
# print("Clientes alocados:", C)
# print("Drones por facilidade:", allocation)
# print("Atendimento:", service)
# print("Cobertura: {:.2f}".format(calc_target_function(wi, service)))

start = time.time()
solution, coverage = genetic_algorithm(m, p, wi, dij, nd, U,
                      pop_size=100, n_iter=200, mutation_rate=0.15,
                      generate_chromo=lambda: open_facilities(n, m, p, wi, dij),
                    )
elapsed = time.time() - start

print(f"Facilities: {solution}")
print(f"Fitness:    {coverage}")
print("Duration:   {time:.2f}s".format(time=elapsed))
