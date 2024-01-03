import sys
import xmlrpc.client
from flask import Flask,request
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)  # Porta diferente para a API Flask, se desejar
