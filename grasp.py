from heuristic import *

def evaluate(m, Jopen, L1, wi, dij, nd, U):
  C = allocate_clients(Jopen, L1, wi, U)

  bij = [[calc_bij(wi[i], dij[i][j]) for j in range(m)] for i in range(len(wi))]

  drones = allocate_drones(nd, Jopen, C, bij)
  service = serve_clients(Jopen, C, bij, drones)

  return calc_target_function(wi, service)

def local_search(m, Jopen, L1, wi, dij, nd, U):
  best_solution = Jopen[:]
  best_f = evaluate(m, best_solution, L1, wi, dij, nd, U)

  for i in range(len(best_solution)):
    for j in range(m):
      if j in best_solution:
        continue

      neighborhood = best_solution[:]
      neighborhood[i] = j
      neighborhood = sorted(neighborhood)

      f = evaluate(m, neighborhood, L1, wi, dij, nd, U)
      if f > best_f:
        best_solution = neighborhood
        best_f = f

  return best_solution, best_f

def grasp(n, m, p, wi, dij, nd, U, n_iter):
  best_solution = None
  best_f = -1

  for _ in range(n_iter):
    Jopen, L1 = open_facilities(n, m, p, wi, dij)
    solution, f = local_search(m, Jopen, L1, wi, dij, nd, U)

    if f > best_f:
      best_solution = solution
      best_f = f

  return best_solution, best_f
