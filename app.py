from flask import Flask, jsonify, send_file, request
import json

import src.ContextBuilder as ContextBuilder
import src.Coordinates as Coordinates
import src.SpeechDecoder as SpeechDecoder
import src.SpeechEncoder as SpeechEncoder
import src.KeysFromText as KeysFromText

app = Flask(__name__)

@app.route("/_healthcheck", methods=['GET'])
def health_check():
    return jsonify(
        ok=True
    )

@app.route('/process', methods=['POST'])
def process():
    speech_decoder = SpeechDecoder.SpeechDecoder()
    keys_from_text = KeysFromText.KeysFromText()
    context_builder = ContextBuilder.ContextBuilder()
    speech_encoder = SpeechEncoder.SpeechEncoder()

    geo = request.form['geo']
    geo = json.loads(geo)

    coordinates = Coordinates.Coordinates()
    coordinates.set_latitude(geo['latitude'])
    coordinates.set_longitude(geo['longitude'])

    text = speech_decoder.decode()
    keys = keys_from_text.keys(text)
    context = context_builder.get_text_context(coordinates, keys)

    print(context)

    return send_file('./mock/default_response.wav')