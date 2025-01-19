import pytest
import sparkplugb_parser as sp


def test_parse_payload_to_dfs(payload_dataset):
    # Ensure that the dataset is parsed correctly
    dfs, properties = sp.parse_payload_to_dfs(payload_dataset)
    assert dfs.shape == (2, 3)
    assert dfs.columns.tolist() == ["Int8s", "Int16s", "Int32s"]
    assert dfs.values.tolist() == [[0, 1, 2], [3, 4, 5]]


def test_parse_payload_to_dfs_empty():
    # Ensure that an exception is raised for an empty payload
    payload = sp.Payload()
    dfs, properties = sp.parse_payload_to_dfs(payload)
    assert dfs is None
