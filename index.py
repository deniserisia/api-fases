from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

def generate_sat_instance(n, m, k):
    """
    Gera uma instância aleatória de k-SAT.
    :param n: Número de variáveis.
    :param m: Número de cláusulas.
    :param k: Número de literais por cláusula.
    :return: Lista de cláusulas.
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
        
        clauses.add(tuple(clause))  # Garante que não há cláusulas duplicadas
    
    return list(clauses)

@app.route("/generate-sat/", methods=["POST"])
def generate_sat():
    """
    Endpoint para gerar uma instância k-SAT e calcular a razão α = m/n.
    """
    data = request.get_json()
    
    try:
        n = int(data["n"])
        m = int(data["m"])
        k = int(data["k"])
    except (KeyError, ValueError):
        return jsonify({"error": "Parâmetros inválidos! Certifique-se de que n, m e k são números inteiros."}), 400

    if k not in [3, 5]:
        return jsonify({"error": "Valor de k inválido! Escolha 3 ou 5."}), 400

    instance = generate_sat_instance(n, m, k)
    alpha = round(m / n, 2)  # Razão cláusulas/variáveis

    return jsonify({
        "n": n,
        "m": m,
        "k": k,
        "alpha": alpha,  # Adicionando a razão α
        "clauses": instance
    })

if __name__ == "__main__":
    app.run(debug=True)
