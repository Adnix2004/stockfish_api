from flask import Flask, request, jsonify
from stockfish import Stockfish
import os

app = Flask(__name__)

# Chemin vers l'exécutable Stockfish (à adapter selon le chemin local)


STOCKFISH_PATH = os.path.join(os.getcwd(), "stockfish_api\engine\stockfish-ubuntu-x86-64-avx2")


# Vérification que le chemin existe
if not os.path.isfile(STOCKFISH_PATH):
    raise FileNotFoundError(f"Le fichier Stockfish est introuvable : {STOCKFISH_PATH}")

# Instanciation globale du moteur Stockfish
stockfish = Stockfish(STOCKFISH_PATH)
@app.route("/get-best-move", methods=["POST"])
def get_best_move():
    data = request.json
    fen = data.get("fen")
    if not fen:
        return jsonify({"error": "FEN manquant"}), 400

    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()

    if not best_move:
        return jsonify({"error": "Impossible de calculer le meilleur coup"}), 500

    return jsonify({"bestmove": best_move})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
