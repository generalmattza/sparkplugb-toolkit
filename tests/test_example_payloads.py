import pytest
from example_payloads import dataset_payload, timeseries_payload
import sparkplugb_parser as sp
import logging

logging.basicConfig(level=logging.DEBUG)


def test_parse_payload_to_dfs():
    # Ensure that the dataset is parsed correctly
    payload = sp.parse_dict_to_protobuf(dataset_payload)
    assert payload.metrics[0].name == "AXUV_example"
    dfs, properties = sp.parse_payload_to_dfs(payload)
    assert dfs.shape == (3, 5)
    assert dfs.columns.tolist() == ["idx", "ch1", "ch2", "ch3", "ch4"]
    assert len(properties["gain"]) == 4
    assert properties["gain"]["ch1"] == 1000
    assert properties["range"] == 5


def test_parse_payload_to_dfs_empty():
    # Ensure that an exception is raised for an empty payload
    payload = sp.Payload()
    dfs, properties = sp.parse_payload_to_dfs(payload)
    assert dfs is None


def test_parse_payload_to_dfs_invalid():
    # Ensure that the dataset is flagged as invalid
    payload = sp.parse_dict_to_protobuf(timeseries_payload)
    dfs, properties = sp.parse_payload_to_dfs(payload)
    assert dfs is None


@pytest.mark.parametrize(
    "example_payload",
    [dataset_payload, timeseries_payload],
    ids=["dataset", "timeseries"],
)
def test_parse_dict_to_protobuf(example_payload):
    # Ensure that the dataset is parsed correctly
    result = sp.parse_dict_to_protobuf(example_payload)
