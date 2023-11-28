# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import synthesis_pb2 as synthesis__pb2


class SmartSpeechStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Synthesize = channel.unary_stream(
                '/smartspeech.synthesis.v1.SmartSpeech/Synthesize',
                request_serializer=synthesis__pb2.SynthesisRequest.SerializeToString,
                response_deserializer=synthesis__pb2.SynthesisResponse.FromString,
                )


class SmartSpeechServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Synthesize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SmartSpeechServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Synthesize': grpc.unary_stream_rpc_method_handler(
                    servicer.Synthesize,
                    request_deserializer=synthesis__pb2.SynthesisRequest.FromString,
                    response_serializer=synthesis__pb2.SynthesisResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'smartspeech.synthesis.v1.SmartSpeech', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SmartSpeech(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Synthesize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/smartspeech.synthesis.v1.SmartSpeech/Synthesize',
            synthesis__pb2.SynthesisRequest.SerializeToString,
            synthesis__pb2.SynthesisResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
