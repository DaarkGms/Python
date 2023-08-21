import numpy as np
from scipy.optimize import linprog

def solve_transportation_problem(costs, supplies, demands):
    num_suppliers = len(supplies)
    num_customers = len(demands)
    
    # Verifica se há oferta e demanda balanceadas
    total_supply = sum(supplies)
    total_demand = sum(demands)
    if total_supply != total_demand:
        raise ValueError("Oferta e demanda não estão balanceadas.")
    
    # Cria a matriz de custos
    cost_matrix = np.array(costs)
    
    # Verifica se a matriz de custos tem o tamanho correto
    if cost_matrix.shape != (num_suppliers, num_customers):
        raise ValueError("Tamanho da matriz de custos incorreto.")
    
    # Adiciona uma oferta ou demanda fictícia, se necessário
    if total_supply > total_demand:
        demands.append(total_supply - total_demand)
        cost_matrix = np.vstack((cost_matrix, np.zeros(num_customers)))
        num_customers += 1
    elif total_demand > total_supply:
        supplies.append(total_demand - total_supply)
        cost_matrix = np.hstack((cost_matrix, np.zeros((num_suppliers, 1))))
        num_suppliers += 1
    
    # Resolve o problema de transporte usando o Simplex
    c = cost_matrix.flatten()
    A_eq = np.zeros((num_suppliers + num_customers, num_suppliers * num_customers))
    b_eq = np.zeros(num_suppliers + num_customers)
    
    # Restrições de oferta
    for i in range(num_suppliers):
        A_eq[i, i * num_customers: (i + 1) * num_customers] = 1
        b_eq[i] = supplies[i]
    
    # Restrições de demanda
    for j in range(num_customers):
        A_eq[num_suppliers + j, j::num_customers] = 1
        b_eq[num_suppliers + j] = demands[j]
    
    bounds = [(0, None)] * (num_suppliers * num_customers)
    
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='simplex')
    
    if not result.success:
        raise ValueError("Não foi possível encontrar uma solução ótima.")
    
    # Formata o resultado em uma matriz de alocação
    allocation = np.reshape(result.x, (num_suppliers, num_customers))
    
    return allocation

# Solicita ao usuário os dados do problema de transporte
num_suppliers = int(input("Informe o número de fornecedores: "))
num_customers = int(input("Informe o número de clientes: "))

costs = []
for i in range(num_suppliers):
    row = list(map(int, input(f"Informe os custos para o fornecedor {i+1}: ").split()))
    costs.append(row)

supplies = list(map(int, input("Informe as ofertas dos fornecedores: ").split()))
demands = list(map(int, input("Informe as demandas dos clientes: ").split()))

# Resolve o problema de transporte
allocation = solve_transportation_problem(costs, supplies, demands)

# Imprime a matriz de alocação
print("Matriz de alocação:")
print(allocation)
