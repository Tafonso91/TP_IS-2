import xmlrpc.client

from flask import Flask,request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000)  # Porta diferente para a API Flask, se desejar
