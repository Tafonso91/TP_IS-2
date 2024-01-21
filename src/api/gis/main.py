import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.database import Database

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

# Crie uma instância da classe Database
db = Database()

CORS(app)

@app.route('/update_country_coords', methods=['PATCH'])
def update_country_coords():
    try:
        data = request.json
        country_name = data.get('country_name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if not country_name or not latitude or not longitude:
            return jsonify({"error": "Faltam dados obrigatórios"}), 400

        update_query = f"UPDATE country SET geom = jsonb_build_object('type', 'Point', 'coordinates', ARRAY[{longitude}, {latitude}]::numeric[]) WHERE country_name = '{country_name}'"
        db.update(update_query)

        return jsonify({"message": "Coordenadas atualizadas com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/get_players_with_coordinates', methods=['GET'])
def get_players_with_coordinates():
    try:
        # Consultar jogadores e coordenadas do país
        players_with_coordinates = db.selectJogadoresComCoordenadas()

        # Formatar a resposta
        result = []
        for player in players_with_coordinates:
            result.append({
                "player_id": player[0],
                "name": player[1],
                "country_id": player[2],
                "coordinates": player[3]
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)

