import pytest
import sparkplug_b_toolkit as spt


def test_parse_payload_to_dfs(example_message_dataset, parser):
    # Ensure that the dataset is parsed correctly
    payload = parser.parse_bytes_to_protobuf(example_message_dataset)
    assert payload.metrics[0].name == "AXUV_example"
    dfs, properties = parser.parse_datasets_to_dfs(payload)
    assert dfs.shape == (3, 5)
    assert dfs.columns.tolist() == ["idx", "ch1", "ch2", "ch3", "ch4"]
    assert len(properties["gain"]) == 4
    assert properties["gain"]["ch1"] == 1000
    assert properties["range"] == 5


def test_parse_payload_to_dfs_empty(parser):
    # Ensure that an exception is raised for an empty payload
    payload = spt.Payload()
    dfs, _ = parser.parse_datasets_to_dfs(payload)
    assert dfs is None


def test_parse_payload_to_dfs_invalid(example_message_timeseries, parser):
    # Ensure that the dataset is flagged as invalid
    payload = parser.parse_bytes_to_protobuf(example_message_timeseries)
    dfs, _ = parser.parse_datasets_to_dfs(payload)
    assert dfs is None
