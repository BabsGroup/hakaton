from flask import Flask, jsonify, request, Response, stream_with_context, send_file
import json
import random
import uuid
import os
import subprocess

import src.Model.Task as Task

import src.ContextBuilder as ContextBuilder
import src.Coordinates as Coordinates
import src.SpeechDecoder as SpeechDecoder
import src.SpeechEncoder as SpeechEncoder
import src.KeysFromText as KeysFromText
import src.GigaChat as GigaChat
import src.Text.voise_text as VoiceText

app = Flask(__name__)

@app.route("/_healthcheck", methods=['GET'])
def health_check():
    return jsonify(
        ok=True
    )

# Сделано с рассчетом на будущую асинхронность
# Сервис может сам захотеть что-то отправить в приложение, ему достаточно будет
# Скинуть ссылку на таску
@app.route('/process/<id>', methods=['GET'])
def process_task(id):
    task = Task.task_by_id(id)
    if task is None:
        return Response() # TODO: Error 404

    coordinates = Coordinates.Coordinates()
    coordinates.set_latitude(task.latitude)
    coordinates.set_longitude(task.longitude)
    print(coordinates.latitude, coordinates.longitude)

    speech_decoder = VoiceText.voise_processing()
    keys_from_text = KeysFromText.KeysFromText()
    context_builder = ContextBuilder.ContextBuilder()
    speech_encoder = SpeechEncoder.SpeechEncoder()
    giga_chat = GigaChat.GigaChat()

    text = speech_decoder.voice(task.filepath)
    keys = keys_from_text.keys(text)
    context = context_builder.get_text_context(coordinates, text, keys)

    answer = giga_chat.createText(text, context)
    print(f"[{id}] text:", text)
    print(f"[{id}] context:", context)
    print(f"[{id}] answer:", answer)

    response_generator = speech_encoder.createSpeech(answer)

    return Response(
        response_generator(),
        content_type='audio/x-wav'
    )

@app.route('/process', methods=['POST'])
def process():
    geo = request.form['geo']
    geo = json.loads(geo)

    coordinates = Coordinates.Coordinates()
    coordinates.set_latitude(geo['latitude'])
    coordinates.set_longitude(geo['longitude'])

    file = request.files['file']
    file_uuid = str(uuid.uuid4())
    tmp_name = f"./tmp/upl/{file_uuid}.mp4"
    result_name = f"./tmp/upl/{file_uuid}.wav"
    file.save(tmp_name)
    subprocess.run(["ffmpeg", "-i", tmp_name, "-ac", "2", "-f", "wav", result_name])
    os.remove(tmp_name)

    task = Task.create_task(
        latitude=coordinates.latitude,
        longitude=coordinates.longitude,
        filepath= result_name
    )

    return jsonify(id=task.id)

if __name__ == "__main__":
    #Task.init_task_table()

    app.run(debug=True, host='0.0.0.0', port=5000)

