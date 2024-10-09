from ortools.linear_solver import pywraplp
import sys

def solve_transport_problem(input_file):
    with open(input_file, 'r') as f:
        n_origins, n_destinations = map(int, f.readline().split())
        production = list(map(int, f.readline().split()))
        demand = list(map(int, f.readline().split()))
        costs = [list(map(int, f.readline().split())) for _ in range(n_origins)]

    solver = pywraplp.Solver.CreateSolver('CBC')

    x = {}
    for i in range(n_origins):
        for j in range(n_destinations):
            x[i, j] = solver.NumVar(0, solver.infinity(), f'x[{i},{j}]')

    # Restrições de oferta
    for i in range(n_origins):
        soma_oferta = 0
        for j in range(n_destinations):
            soma_oferta += x[i, j]
        solver.Add(soma_oferta <= production[i])
        
    # Restrições de demanda
    for j in range(n_destinations):
        soma_demanda = 0
        for i in range(n_origins):
            soma_demanda += x[i, j]
        solver.Add(soma_demanda >= demand[j])

    objective = solver.Objective()
    for i in range(n_origins):
        for j in range(n_destinations):
            objective.SetCoefficient(x[i, j], costs[i][j])
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Política de transporte:")
        for i in range(n_origins):
            for j in range(n_destinations):
                if x[i, j].solution_value() > 0:
                    print(f"Transporte de {int(x[i, j].solution_value())} unidades da origem {i+1} para o destino {j+1}.")
        print(f"\nCusto total: {solver.Objective().Value()}")
    else:
        print("O problema não tem solução ótima.")

if __name__ == "__main__":
    input_file = sys.argv[1]
    solve_transport_problem(input_file)