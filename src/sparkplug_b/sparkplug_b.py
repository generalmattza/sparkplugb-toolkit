import sparkplug_b.sparkplug_b_pb2 as sparkplug_b_pb2
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToDict

# Create a new payload
payload = sparkplug_b_pb2.Payload()


def build_payload(protobuf):
    packet = MessageToDict(protobuf)
    return packet


def build_protobuf(packet: dict):
    payload = sparkplug_b_pb2.Payload()
    ParseDict(packet, payload)
    return payload
