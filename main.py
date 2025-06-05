from entrada import *
from distancia import *
from heuristica import *

wi = [d["Demand (kg)"] for d in demandas]
dij = []

for demanda in demandas:
  row = []

  for candidato in candidatos:
    distancia = calcular_distancia(
      demanda["Latitude"], demanda["Longitude"],
      candidato["Latitude"], candidato["Longitude"]
    )
    row.append(distancia)

  dij.append(row)

n, m, p, nd = len(wi), len(candidatos), 25, 25
U = sum(wi) / (0.8 * p)

Jopen, L_copy = abrir_facilidades(n, m, p, wi, dij)
C = alocar_clientes(Jopen, L_copy, wi, U)

bij_matrix = np.array([[calc_bij(wi[i], dij[i][j]) for j in range(m)] for i in range(n)])

drones = alocar_drones(Jopen, C, bij_matrix, B, nd)
entregas = atender_clientes(Jopen, C, bij_matrix, B, drones)

print("Facilidades abertas:", Jopen)
print("Clientes alocados:", C)
print("Drones por facilidade:", drones)
print("Entregas:", entregas)
print("Demanda atendida: {:.2f}%".format(calcular_demanda_atendida(wi, entregas)))
