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


@pytest.fixture
def payload_dataset():
    # Define a dataset type payload
    payload = sp.Payload()
    types = [
        sp.DataSetDataType.Int8,
        sp.DataSetDataType.Int16,
        sp.DataSetDataType.Int32,
    ]
    columns = ["Int8s", "Int16s", "Int32s"]
    dataset = sp.init_dataset_metric(payload, "Dataset Metric", types, columns)
    sp.add_rows_to_dataset(dataset, [[0, 1, 2], [3, 4, 5]])
    return payload
