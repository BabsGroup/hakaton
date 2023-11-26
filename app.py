from flask import Flask, jsonify, send_file

app = Flask(__name__)

@app.route("/_healthcheck", methods=['GET'])
def health_check():
    return jsonify(
        ok=True
    )

@app.route('/process', methods=['POST'])
def process():
    return send_file('./mock/default_response.wav')