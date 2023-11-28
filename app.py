from flask import Flask, jsonify, request, Response, stream_with_context, send_file
import json

import src.ContextBuilder as ContextBuilder
import src.Coordinates as Coordinates
import src.SpeechDecoder as SpeechDecoder
import src.SpeechEncoder as SpeechEncoder
import src.KeysFromText as KeysFromText
import src.GigaChat as GigaChat

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
    giga_chat = GigaChat.GigaChat()

    geo = request.form['geo']
    geo = json.loads(geo)

    coordinates = Coordinates.Coordinates()
    coordinates.set_latitude(geo['latitude'])
    coordinates.set_longitude(geo['longitude'])

    text = speech_decoder.decode()

    keys = keys_from_text.keys(text)
    context = context_builder.get_text_context(coordinates, keys)

    print("text:", text)
    print("context:", context)
    answer = giga_chat.createText(text, context)
    print("answer:", answer)

    response = speech_encoder.createSpeech(answer)

    return send_file(response)
    # def generate():
    #     sum = 0
    #     for chunk in response.iter_content(chunk_size=64*1024):
    #         sum = sum + len(chunk)
    #         if chunk:
    #             yield chunk
    #     print(sum)
    #
    # return Response(
    #     generate(),
    #     content_type='audio/x-wav'
    # )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)