import random

from heuristic import *

def init_population(pop_size, m, p, generate_chromo):
  population = []
  L1 = None

  for _ in range(pop_size // 2):
    chromo = random.sample(range(m), p)
    population.append(chromo)

  for _ in range(pop_size // 2):
    chromo, L1 = generate_chromo()
    population.append(chromo)

  return population, L1

def evaluate_population(population, L1, wi, dij, nd, U):
  evaluations = []

  for chromo in population:
    Jopen = chromo
    C = allocate_clients(Jopen, L1, wi, U)
    bij = [[calc_bij(wi[i], dij[i][j]) for j in range(len(dij[0]))] for i in range(len(wi))]
    drones = allocate_drones(nd, Jopen, C, bij)
    service = serve_clients(Jopen, C, bij, drones)

    f = calc_target_function(wi, service)
    evaluations.append((chromo, f))

  return evaluations

def selection(eval_population):
  new_population = []

  while len(new_population) < len(eval_population):
    c1, c2 = random.sample(eval_population, 2)
    best = c1 if c1[1] > c2[1] else c2
    new_population.append(best[0])

  return new_population

def crossover(p1, p2, p):
  common = list(set(p1) & set(p2))
  remaining = list(set(p1 + p2) - set(common))

  random.shuffle(remaining)

  children = []

  for _ in range(2):
    child = common[:]

    while len(child) < p:
      random_gene = remaining.pop()

      if random_gene not in child:
        child.append(random_gene)

    children.append(child)

  return children[0], children[1]

def mutation(chromo, m, p, rate):
  if random.random() < rate:
    new_chromo = chromo[:]
    random_facility = random.choice([j for j in range(m) if j not in new_chromo])

    i = random.randint(0, p - 1)
    new_chromo[i] = random_facility

    return new_chromo

  return chromo

def genetic_algorithm(
  m, p, wi, dij, nd, U,
  pop_size, n_iter, mutation_rate,
  generate_chromo,
):
  population, L1 = init_population(pop_size, m, p, generate_chromo)

  best_solution = None
  best_fitness = -1

  for _ in range(n_iter):
    eval_population = evaluate_population(population, L1, wi, dij, nd, U)

    for solution, fitness in eval_population:
      if fitness > best_fitness:
        best_solution = solution
        best_fitness = fitness

    parents = selection(eval_population)
    new_population = []

    for i in range(0, len(parents), 2):
      p1, p2 = parents[i], parents[i + 1]
      c1, c2 = crossover(p1, p2, p)

      new_population.append(mutation(c1, m, p, mutation_rate))
      new_population.append(mutation(c2, m, p, mutation_rate))

    population = new_population

  return best_solution, best_fitness
