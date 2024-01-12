import sys
import xmlrpc.client
from flask import Flask,request,jsonify
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
app = Flask(__name__)
CORS(app)

# Endpoint na sua API Flask para chamar a função do servidor XML-RPC
@app.route('/api/players_country', methods=['GET'])
def get_players_by_country():
    # Configurações do servidor XML-RPC
    server_url = 'http://rpc-server:9000'  # Substitua pelo seu URL do servidor XML-RPC
    server = xmlrpc.client.ServerProxy(server_url)
    nome_pais=request.args.get("nome_pais")
    # Chama a função no servidor XML-RPC
    players = server.fetch_players_by_country(nome_pais)

    # Retorna os dados obtidos pela função diretamente na resposta
    return players

@app.route('/api/countries', methods=['GET'])
def get_countries():
    # Configurações do servidor XML-RPC
    server_url = 'http://rpc-server:9000'  # Substitua pelo seu URL do servidor XML-RPC
    server = xmlrpc.client.ServerProxy(server_url)
    # Chama a função no servidor XML-RPC
    countries = server.lista_paises()

    # Retorna os dados obtidos pela função diretamente na resposta
    return countries

@app.route('/api/players_club', methods=['GET'])
def get_players_by_club():
    # Configurações do servidor XML-RPC
    server_url = 'http://rpc-server:9000'  # Substitua pelo seu URL do servidor XML-RPC
    server = xmlrpc.client.ServerProxy(server_url)
    nome_club=request.args.get("nome_club")
    # Chama a função no servidor XML-RPC
    jogadores = server.fetch_players_by_club(nome_club)

    # Retorna os dados obtidos pela função diretamente na resposta
    return jogadores
@app.route('/api/clubs', methods=['GET'])
def get_clubs():
    # Configurações do servidor XML-RPC
    server_url = 'http://rpc-server:9000'  # Substitua pelo seu URL do servidor XML-RPC
    server = xmlrpc.client.ServerProxy(server_url)
    # Chama a função no servidor XML-RPC
    clubs = server.lista_clubes()

    # Retorna os dados obtidos pela função diretamente na resposta
    return clubs

@app.route('/api/players', methods=['GET'])
def get_players():
    # Configurações do servidor XML-RPC
    server_url = 'http://rpc-server:9000'  # Substitua pelo seu URL do servidor XML-RPC
    server = xmlrpc.client.ServerProxy(server_url)
    # Chama a função no servidor XML-RPC
    players = server.lista_todos_jogadores()

    # Retorna os dados obtidos pela função diretamente na resposta
    return players

@app.route('/api/feet', methods=['GET'])
def get_feet():
    # Configurações do servidor XML-RPC
    server_url = 'http://rpc-server:9000'  # Substitua pelo seu URL do servidor XML-RPC
    server = xmlrpc.client.ServerProxy(server_url)
    # Chama a função no servidor XML-RPC
    feet = server.lista_pe()

    # Retorna os dados obtidos pela função diretamente na resposta
    return feet

@app.route('/api/top_players', methods=['GET'])
def get_top_players():
    # Configurações do servidor XML-RPC
    server_url = 'http://rpc-server:9000'  # Substitua pelo seu URL do servidor XML-RPC
    server = xmlrpc.client.ServerProxy(server_url)
    # Chama a função no servidor XML-RPC
    top_players = server.lista_top_jogadores()

    # Retorna os dados obtidos pela função diretamente na resposta
    return top_players

@app.route('/api/pt_players', methods=['GET'])
def get_pt_players():
    # Configurações do servidor XML-RPC
    server_url = 'http://rpc-server:9000'  # Substitua pelo seu URL do servidor XML-RPC
    server = xmlrpc.client.ServerProxy(server_url)

    # Chama a função no servidor XML-RPC
    pt_players = server.lista_promessas_portugal()

    # Converte a lista de tuplas para um formato que pode ser serializado para JSON
    players_data = [{
        "potencial": potencial,
        "nome": nome,
        "overall": overall,
        "height": height,
        "price": price,
        "salary": salary
    } for potencial, nome, overall, height, price, salary in pt_players]

    # Retorna os dados em formato JSON
    return jsonify(players_data)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)  # Porta diferente para a API Flask, se desejar
