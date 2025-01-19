import sparkplugb_parser as sp


def test_parse_message_to_protobuf(payload):
    payload_string = sp.parse_protobuf_to_message(payload)
    result = sp.parse_message_to_protobuf(payload_string)
    assert result == payload
    assert result.metrics[0].name == "Node Metric0"
    assert result.metrics[0].datatype == 0
    assert result.metrics[0].string_value == "hello node"
    assert result.metrics[1].name == "Node Metric1"
    assert result.metrics[1].datatype == 1
    assert result.metrics[1].boolean_value == True


def test_parse_protobuf_to_message(message):
    payload = sp.parse_message_to_protobuf(message)
    result = sp.parse_protobuf_to_message(payload)
    assert result == message
