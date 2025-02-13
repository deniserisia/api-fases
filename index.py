from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import numpy as np
from pysat.solvers import Solver

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

def generate_clause(n, k):
    """Gera uma cláusula aleatória com k literais, sem repetições ou contradições."""
    clause = set()
    while len(clause) < k:
        var = random.randint(1, n)
        negated = random.choice([True, False])
        literal = -var if negated else var
        if -literal not in clause:
            clause.add(literal)
    return list(clause)

def generate_sat_instance(n, m, k):
    """Gera uma instância aleatória de k-SAT."""
    return [generate_clause(n, k) for _ in range(m)]

def is_satisfiable(clauses):
    """Determina se uma instância é satisfazível usando o solver PySAT."""
    solver = Solver(name='glucose3')
    for clause in clauses:
        solver.add_clause(clause)
    result = solver.solve()
    solver.delete()
    return result

@app.route('/generate-sat/', methods=['POST'])
def generate_sat_endpoint():
    data = request.get_json()
    n = data.get('n', 50)
    m = data.get('m', 100)
    k = data.get('k', 3)

    if k not in [3, 5]:
        return jsonify({'error': 'O valor de k deve ser 3 ou 5'}), 400

    clauses = generate_sat_instance(n, m, k)
    alpha = m / n

    return jsonify({'clauses': clauses, 'alpha': alpha})

def generate_sat_instance(n, m, k):
    """
    Gera uma instância aleatória de k-SAT.
    """
    clauses = set()
    while len(clauses) < m:
        clause = set()
        while len(clause) < k:
            literal = random.randint(1, n)
            if random.random() < 0.5:
                literal = -literal
            if -literal not in clause:
                clause.add(literal)
        clauses.add(tuple(clause))
    return list(clauses)

def is_satisfiable(clauses):
    """
    Determina se uma instância é satisfazível usando o solver PySAT.
    """
    solver = Solver(name='glucose3')
    for clause in clauses:
        solver.add_clause(clause)
    result = solver.solve()
    solver.delete()
    return result

@app.route('/graph-data/', methods=['GET'])
def get_graph_data():
    """
    Gera e retorna os dados do gráfico JSON.
    """
    n_values = [50, 100, 150, 200]
    alpha_values = np.linspace(3.5, 4.7, 10)
    num_instances = 50

    graph_data = []
    
    for n in n_values:
        probabilities = []
        for alpha in alpha_values:
            m = int(alpha * n)
            satisfiable_count = sum(is_satisfiable(generate_sat_instance(n, m, 3)) for _ in range(num_instances))
            probability = satisfiable_count / num_instances
            probabilities.append(probability)
        
        graph_data.append({
            "n": n,
            "alpha_values": alpha_values.tolist(),
            "probabilities": probabilities
        })

    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(debug=True)
