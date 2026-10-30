# Importa as ferramentas que vamos usar
from flask import Flask, jsonify  # Flask cria a API; jsonify devolve JSON
import requests                    # requests faz a consulta à BrasilAPI

# Cria a aplicação
app = Flask(__name__)

# Endereço base da BrasilAPI
URL_BASE = "https://brasilapi.com.br/api"


# Rota 1: consulta dados de um CEP -> http://127.0.0.1:5000/cep/01310100
@app.route("/cep/<cep>")
def consultar_cep(cep):
    # Trata a entrada removendo pontuações e traços
    cep_limpo = ''.join(filter(str.isdigit, cep))
    
    resposta = requests.get(f"{URL_BASE}/cep/v2/{cep_limpo}")
    
    if resposta.status_code == 404:
        return jsonify({"erro": "CEP não encontrado"}), 404
    elif resposta.status_code != 200:
        return jsonify({"erro": "Falha ao consultar a API"}), 502

    return jsonify(resposta.json())


# Rota 2: consulta dados de uma empresa por CNPJ -> http://127.0.0.1:5000/cnpj/00000000000191
@app.route("/cnpj/<cnpj>")
def consultar_cnpj(cnpj):
    # Trata a entrada removendo barras, pontos e traços
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    
    resposta = requests.get(f"{URL_BASE}/cnpj/v1/{cnpj_limpo}")
    
    if resposta.status_code == 404:
        return jsonify({"erro": "CNPJ não encontrado"}), 404
    elif resposta.status_code != 200:
        return jsonify({"erro": "Falha ao consultar a API"}), 502

    return jsonify(resposta.json())


# Rota 3: consulta cidades e estado por DDD -> http://127.0.0.1:5000/ddd/47
@app.route("/ddd/<ddd>")
def consultar_ddd(ddd):
    resposta = requests.get(f"{URL_BASE}/ddd/v1/{ddd}")
    
    if resposta.status_code == 404:
        return jsonify({"erro": "DDD não encontrado"}), 404
    elif resposta.status_code != 200:
        return jsonify({"erro": "Falha ao consultar a API"}), 502

    return jsonify(resposta.json())


# Rota 4: lista todos os bancos do Brasil -> http://127.0.0.1:5000/bancos
@app.route("/bancos")
def listar_bancos():
    resposta = requests.get(f"{URL_BASE}/banks/v1")
    
    if resposta.status_code != 200:
        return jsonify({"erro": "Falha ao consultar a API"}), 502

    return jsonify(resposta.json())


# Roda o servidor quando executamos: python app.py
if __name__ == "__main__":
    app.run(debug=True)