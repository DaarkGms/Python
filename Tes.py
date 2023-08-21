from pulp import *
import os 
# Solicita ao usuário os dados do problema
num_vars = int(input("Quantas variáveis ​​existem no problema? "))
num_const = int(input("Quantas restrições existem no problema? "))
os.system('cls') or None

# Cria um problema do PuLP
prob = LpProblem("Problema de Programação Linear", LpMaximize)

# Cria as variáveis ​​do problema
x = LpVariable.dicts("x", list(range(1, num_vars+1)), lowBound=0, cat='Continuous')

# Cria as restrições do problema
for i in range(1, num_const+1):
    constraint = input(f"Informe a {i}ª restrição (separando os coeficientes e o lado direito com espaços): ")
    coeffs = [float(c) for c in constraint.split()[:-1]]
    rhs = float(constraint.split()[-1])
    prob += lpDot(coeffs, x.values()) <= rhs

# Define a função objetivo do problema
objective = input("Informe a função objetivo (separando os coeficientes com espaços): ")
obj_coeffs = [float(c) for c in objective.split()]
prob += lpDot(obj_coeffs, x.values())

# Resolve o problema usando o método Simplex
prob.solve()

# Imprime a solução ótima
os.system('cls') or None
print("Status:", LpStatus[prob.status])
print("Valor ótimo:", value(prob.objective))
print("Solução ótima:")
for v in prob.variables():
    print(v.name, "=", v.varValue)
