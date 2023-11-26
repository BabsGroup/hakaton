from flask import Flask, jsonify, send_file
import src.ContextBuilder as ContextBuilder
import src.Keys as Keys
import src.Coordinates as Coordinates

app = Flask(__name__)

@app.route("/_healthcheck", methods=['GET'])
def health_check():
    return jsonify(
        ok=True
    )

@app.route('/process', methods=['POST'])
def process():
    k = Keys.Keys()
    k.set_type('парк')

    coordinates = Coordinates.Coordinates()
    coordinates.set_latitude(55.705558)
    coordinates.set_longitude(37.534199)

    context_builder = ContextBuilder.ContextBuilder()
    context = context_builder.get_text_context(coordinates, k)
    print(context)

    return send_file('./mock/default_response.wav')