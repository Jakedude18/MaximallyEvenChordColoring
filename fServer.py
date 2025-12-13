from flask import Flask, request, jsonify, send_from_directory
import chordColorer
import os

app = Flask(__name__)

@app.route("/compute_chord", methods=["POST"])
def compute_chord():
    data = request.json

    # Ensure baseChord and mode are integers modulo 12, sorted ascending
    baseChord = sorted([int(pc) % 12 for pc in data.get("baseChord", [])])
    mode = sorted([int(pc) % 12 for pc in data.get("mode", [0,2,4,5,7,9,11])])
    onsets = int(data.get("onsets", 6))

    
    print(f"Received request:\n  baseChord={baseChord}\n  mode={mode}\n  onsets={onsets}")

    # Call proto.py with proper parameters
    try:
        coloring, evennessScore = chordColorer.maximizeColoring(baseChord, mode, onsets)
        if coloring is None:
            coloring = []
    except Exception as e:
        return jsonify({"error": str(e), "coloring": []})

    return jsonify({
            "bestColoring": coloring,
            "maxEvenness": evennessScore
        })
# serve the HTML/JS frontend
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")

if __name__ == "__main__":
    app.run(debug=True)
    
