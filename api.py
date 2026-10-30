# Importa as ferramentas
from flask import Flask, jsonify  # Flask cria a API; jsonify devolve JSON
import requests                    # requests faz a consulta à PokéAPI

# Cria a aplicação
app = Flask(__name__)

# Endereço base da PokéAPI
URL_BASE = "https://pokeapi.co/api/v2/pokemon"


# Rota 1: busca dados de um Pokémon específico -> http://127.0.0.1:5000/pokemon/pikachu
@app.route("/pokemon/<nome>")
def obter_pokemon(nome):
    resposta = requests.get(f"{URL_BASE}/{nome.lower().strip()}")
    
    if resposta.status_code == 404:
        return jsonify({"erro": "Pokémon não encontrado"}), 404
    elif resposta.status_code != 200:
        return jsonify({"erro": "Falha ao consultar a PokéAPI"}), 502

    dados = resposta.json()

    # Formata a resposta trazendo apenas as informações principais
    pokemon_info = {
        "id": dados["id"],
        "nome": dados["name"],
        "altura": dados["height"],
        "peso": dados["weight"],
        "tipos": [t["type"]["name"] for t in dados["types"]]
    }

    return jsonify(pokemon_info)


# Rota 2: lista os primeiros 20 Pokémons -> http://127.0.0.1:5000/pokemon
@app.route("/pokemon")
def listar_pokemons():
    resposta = requests.get(f"{URL_BASE}?limit=20")
    
    if resposta.status_code != 200:
        return jsonify({"erro": "Falha ao consultar a PokéAPI"}), 502

    dados = resposta.json()

    lista = []
    for item in dados["results"]:
        lista.append({"nome": item["name"]})

    return jsonify({"total": len(lista), "pokemons": lista})


# Roda o servidor
if __name__ == "__main__":
    app.run(debug=True)