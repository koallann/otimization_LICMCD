from heuristica import *
import random

def inicializar_populacao(pop_size, m, p, gerar_individuo_por_heuristica):
  populacao = []
  L_copy = None

  for _ in range(pop_size // 2):
    individuo = random.sample(range(m), p)
    populacao.append(individuo)

  for _ in range(pop_size // 2):
    individuo, L_copy = gerar_individuo_por_heuristica()
    populacao.append(individuo)

  return populacao, L_copy

def avaliar_populacao(populacao, L_copy, wi, dij, B, nd, capacidade_U):
  avaliacoes = []

  for individuo in populacao:
    Jopen = individuo
    C = alocar_clientes(Jopen, L_copy, wi, capacidade_U)

    bij = [[calc_bij(wi[i], dij[i][j]) for j in range(len(dij[0]))] for i in range(len(wi))]

    drones = alocar_drones(Jopen, C, bij, B, nd)
    atendimento = atender_clientes(Jopen, C, bij, B, drones)
    f = calcular_funcao_objetivo(wi, atendimento)
    avaliacoes.append((individuo, f))

  return avaliacoes

def selecao_torneio(pop_avaliada):
  nova_pop = []

  while len(nova_pop) < len(pop_avaliada):
    i1, i2 = random.sample(pop_avaliada, 2)
    melhor = i1 if i1[1] > i2[1] else i2
    nova_pop.append(melhor[0])

  return nova_pop

def crossover(p1, p2, m, p):
  comuns = list(set(p1) & set(p2))
  restantes = list(set(p1 + p2) - set(comuns))
  random.shuffle(restantes)
  filhos = []

  for _ in range(2):
    f = comuns[:]

    while len(f) < p:
      g = restantes.pop()

      if g not in f:
        f.append(g)

    filhos.append(f)

  return filhos

def mutacao(individuo, m, p, taxa):
  if random.random() < taxa:
    nova = individuo[:]
    i = random.randint(0, p - 1)
    nova_inst = random.choice([j for j in range(m) if j not in nova])
    nova[i] = nova_inst

    return nova

  return individuo

def algoritmo_genetico(
  m, p, wi, dij, nd, U,
  pop_size, n_iter, taxa_mutacao,
  gerar_individuo_por_heuristica,
):
  pop, L_copy = inicializar_populacao(pop_size, m, p, gerar_individuo_por_heuristica)

  melhor_solucao = None
  melhor_fit = -1

  for _ in range(n_iter):
    pop_avaliada = avaliar_populacao(pop, L_copy, wi, dij, B, nd, U)

    for solucao, fit in pop_avaliada:
      if fit > melhor_fit:
        melhor_solucao = solucao
        melhor_fit = fit

    pais = selecao_torneio(pop_avaliada)
    nova_pop = []

    for i in range(0, len(pais), 2):
      p1, p2 = pais[i], pais[i + 1]
      f1, f2 = crossover(p1, p2, m, p)
      nova_pop.append(mutacao(f1, m, p, taxa_mutacao))
      nova_pop.append(mutacao(f2, m, p, taxa_mutacao))

    pop = nova_pop

  return melhor_solucao, melhor_fit
