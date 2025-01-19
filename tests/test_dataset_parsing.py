import pytest
import sparkplug_b as sp


def test_parse_payload_to_dfs(payload_dataset):
    # Ensure that the dataset is parsed correctly
    result = sp.parse_payload_to_dfs(payload_dataset)
    assert result.shape == (2, 3)
    assert result.columns.tolist() == ["Int8s", "Int16s", "Int32s"]
    assert result.values.tolist() == [[0, 1, 2], [3, 4, 5]]


def test_parse_payload_to_dfs_empty():
    # Ensure that an exception is raised for an empty payload
    payload = sp.Payload()
    with pytest.raises(AssertionError):
        result = sp.parse_payload_to_dfs(payload)
