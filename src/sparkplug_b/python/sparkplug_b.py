import sparkplug_b.python.sparkplug_b_pb2 as sparkplug_b_pb2
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import DecodeError, EncodeError


def parse_message_to_protobuf(message: bytearray) -> sparkplug_b_pb2.Payload:
    # Parse serialized payload data from message
    payload = sparkplug_b_pb2.Payload()
    try:
        payload.ParseFromString(message)
    except DecodeError as e:
        print(f"Error decoding payload: {e}")
    return payload


def parse_dict_to_protobuf(packet: dict) -> sparkplug_b_pb2.Payload:
    # Create a new payload
    payload = sparkplug_b_pb2.Payload()
    # Parse the dictionary into the payload
    ParseDict(packet, payload)
    return payload


def parse_message_to_dict(message: bytes) -> dict:
    # Parse the payload into a dictionary
    packet = MessageToDict(
        message,
        preserving_proto_field_name=True,
        use_integers_for_enums=False,
        float_precision=None,
    )
    return packet


def parse_protobuf_to_message(protobuf: sparkplug_b_pb2.Payload) -> bytes:
    # Serialize the payload to a message in bytes
    message = protobuf.SerializeToString()
    message = bytearray(message)
    return message
