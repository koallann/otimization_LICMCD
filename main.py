from entrada import *
from distancia import *
from heuristica import *
from algoritmo_genetico import *
import time

wi = [d["Demand (kg)"] for d in demandas]
dij = []

for d in demandas:
  row = []

  for c in candidatos:
    dist = calcular_distancia(
      d["Latitude"], d["Longitude"],
      c["Latitude"], c["Longitude"],
    )
    row.append(dist)

  dij.append(row)


n = len(wi)
m = len(candidatos)
p = 25 # quantidade de instalações
nd = 100 # quantidade de drones
U = sum(wi) / (0.8 * p)

start = time.time()

melhor_solucao, melhor_fit = algoritmo_genetico(
  m=m, p=p, wi=wi, dij=dij, nd=nd, U=U,
  pop_size=100, n_iter=200, taxa_mutacao=0.15,
  gerar_individuo_por_heuristica=lambda: abrir_facilidades(n, m, p, wi, dij, t=5),
)

elapsed = time.time() - start

print("Instalações:", melhor_solucao)
print("Cobertura:", melhor_fit)
print("Tempo: {time:.2f}s".format(time=elapsed))

# USO:
# Jopen, L_copy = abrir_facilidades(n, m, p, wi, dij)
# C = alocar_clientes(Jopen, L_copy, wi, U)
# bij = np.array([[calc_bij(wi[i], dij[i][j]) for j in range(m)] for i in range(n)])
# drones = alocar_drones(Jopen, C, bij, B, nd)
# atendimento = atender_clientes(Jopen, C, bij, B, drones)

# print("Facilidades abertas:", Jopen)
# print("Clientes alocados:", C)
# print("Drones por facilidade:", drones)
# print("Atendimento:", atendimento)
# print("Demanda atendida: {:.2f}%".format(calcular_funcao_objetivo(wi, atendimento)))
