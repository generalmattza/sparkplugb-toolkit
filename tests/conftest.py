import pytest
import sparkplug_b as sp


@pytest.fixture
def payload():
    payload = sp.Payload()
    payload.metrics.add().name = "Node Metric0"
    payload.metrics[0].datatype = 0
    payload.metrics[0].string_value = "hello node"
    payload.metrics.add().name = "Node Metric1"
    payload.metrics[1].datatype = 1
    payload.metrics[1].boolean_value = True
    return payload


@pytest.fixture
def message(payload):
    message = sp.parse_protobuf_to_message(payload)
    return message
