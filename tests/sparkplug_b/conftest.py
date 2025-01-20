import pytest
import sparkplug_b_toolkit as spt
from sparkplug_b_toolkit.example_payloads import example_payloads


@pytest.fixture(scope="module")
def parser():
    return spt.SparkplugBParser()


@pytest.fixture(scope="module")
def example_message_json(parser):
    message = parser.parse_dict_to_bytes(example_payloads["json"])
    return message


@pytest.fixture(scope="module")
def example_message_dataset(parser):
    message = parser.parse_dict_to_bytes(example_payloads["dataset"])
    return message


@pytest.fixture(scope="module")
def example_message_timeseries(parser):
    message = parser.parse_dict_to_bytes(example_payloads["timeseries"])
    return message
