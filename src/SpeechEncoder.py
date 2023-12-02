import requests
import random
import uuid
import shutil

import grpc

import synthesis_pb2
import synthesis_pb2_grpc

ENCODING_PCM = 'pcm'
ENCODING_OPUS = 'opus'
ENCODING_WAV = 'wav'
ENCODINGS_MAP = {
    ENCODING_PCM: synthesis_pb2.SynthesisRequest.PCM_S16LE,
    ENCODING_OPUS: synthesis_pb2.SynthesisRequest.OPUS,
    ENCODING_WAV: synthesis_pb2.SynthesisRequest.WAV,
}

TYPE_TEXT = 'text'
TYPE_SSML = 'ssml'
TYPES_MAP = {
    TYPE_TEXT: synthesis_pb2.SynthesisRequest.TEXT,
    TYPE_SSML: synthesis_pb2.SynthesisRequest.SSML,
}


def synthesize(token, text, file):
    scc = grpc.ssl_channel_credentials(
        root_certificates=open('./russiantrustedca.pem', 'rb').read(),
    )

    tok = grpc.access_token_call_credentials(token)
    ccc = grpc.composite_channel_credentials(scc, tok)

    channel = grpc.secure_channel("smartspeech.sber.ru", ccc)

    stub = synthesis_pb2_grpc.SmartSpeechStub(channel)

    options = synthesis_pb2.SynthesisRequest()
    setattr(options, TYPE_TEXT, text)
    con = stub.Synthesize(options)

    try:
        buffer = None
        for resp in con:
            if buffer is None:
                buffer = resp.data
            else:
                buffer += resp.data

            if buffer is not None and len(buffer) > 1024 * 32:
                yield buffer
                buffer = None

        if buffer is not None:
            yield buffer

    except grpc.RpcError as err:
        print('RPC error: code = {}, details = {}'.format(err.code(), err.details()))
    except Exception as exc:
        print('Exception:', exc)
    else:
        print('Synthesis has finished')
    finally:
        channel.close()

class SpeechEncoder:
    def __init__(self):
        pass

    def createSpeech(self, text):
        r = requests.post(
            'https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
            data={'scope': 'SALUTE_SPEECH_PERS'},
            headers={
                'Authorization': "Basic ZDFlM2ZmM2MtNDQ4MC00ZmViLTgxNjgtOGYwZTBiZTkzZThiOjZkMDIzZWI0LTQwNmEtNGFkZC1hOGUwLTVhYTllMDhiNmYxOQ==",
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'RqUID': str(uuid.uuid4()),
            },
            verify = False,
        )

        token = r.json()['access_token']
        file = f"./tmp/{random.randint(0, 1000000)}.wav"

        def generator():
            return synthesize(token, text, file)

        return generator
