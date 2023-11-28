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

    channel = grpc.secure_channel(
        "smartspeech.sber.ru",
        ccc
    )

    stub = synthesis_pb2_grpc.SmartSpeechStub(channel)

    options = synthesis_pb2.SynthesisRequest()
    setattr(options, TYPE_TEXT, text)
    con = stub.Synthesize(options)

    try:
        with open(file, 'wb') as f:
            for resp in con:
                f.write(resp.data)
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

        synthesize(token, text, file)

        return file
        # return requests.post(
        #     'https://smartspeech.sber.ru/rest/v1/text:synthesize?format=wav16&voice=Nec_24000',
        #     data=text,
        #     headers={
        #         'Authorization': f"Bearer {r.json()['access_token']}",
        #         'Content-Type': 'application/ssml',
        #     },
        #     verify=False,
        #     stream=True,
        # )
