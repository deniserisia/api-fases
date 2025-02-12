from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar a extensão CORS
import random

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

class SATRequest:
    def __init__(self, n, m, k):
        self.n = n
        self.m = m
        self.k = k

def generate_sat_instance(n, m, k):
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

@app.route("/generate-sat/", methods=["POST"])
def generate_sat():
    data = request.get_json()
    n, m, k = data["n"], data["m"], data["k"]
    
    if k not in [3, 5]:
        return jsonify({"error": "Valor de k inválido! Escolha 3 ou 5."}), 400
    
    instance = generate_sat_instance(n, m, k)
    return jsonify({"n": n, "m": m, "k": k, "clauses": instance})

if __name__ == "__main__":
    app.run(debug=True)
