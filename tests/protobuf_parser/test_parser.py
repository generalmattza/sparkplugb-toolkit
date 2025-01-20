import pytest
from google.protobuf.struct_pb2 import Struct

from protobuf_facade import ProtobufParser


# 1. Define a subclass of ProtobufParser that uses Struct as the message type.
class StructParser(ProtobufParser[Struct]):
    message_type = Struct


@pytest.fixture
def parser():
    """
    Returns an instance of StructParser for testing.
    """
    return StructParser()


@pytest.fixture
def example_dict():
    """
    A sample Python dict that can be converted into a Struct.
    Struct supports nested keys, so let's use a nested structure.
    """
    return {
        "name": "test",
        "count": 42,
        "nested": {
            "enabled": True,
            "values": [1, 2, 3],
        },
    }


@pytest.fixture
def serialized_bytes(example_dict, parser):
    """
    Returns raw bytes by converting the example_dict into a Struct,
    then serializing that Struct.
    """
    return parser.parse_dict_to_bytes(example_dict)


# ----------------------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------------------


def test_parse_dict_to_protobuf(parser, example_dict):
    """
    Ensure parse_dict_to_protobuf returns a Struct containing
    the expected fields.
    """
    struct_obj = parser.parse_dict_to_protobuf(example_dict)
    assert isinstance(struct_obj, Struct)
    # Check a few fields
    assert struct_obj.fields["name"].string_value == "test"
    assert struct_obj.fields["count"].number_value == 42

    # Check nested
    nested_struct = struct_obj.fields["nested"].struct_value
    assert nested_struct.fields["enabled"].bool_value is True
    # arrays (lists) in Struct appear as list_value
    list_val = nested_struct.fields["values"].list_value
    assert [x.number_value for x in list_val.values] == [1, 2, 3]


def test_parse_protobuf_to_bytes(parser, example_dict):
    """
    Check we can convert a Struct to bytes.
    """
    # 1. Dict -> Struct
    struct_obj = parser.parse_dict_to_protobuf(example_dict)
    # 2. Struct -> bytes
    raw_bytes = parser.parse_protobuf_to_bytes(struct_obj)
    assert isinstance(raw_bytes, bytes)
    assert len(raw_bytes) > 0


def test_parse_bytes_to_protobuf(parser, serialized_bytes):
    """
    Validate we can parse bytes back into a Struct object.
    """
    struct_obj = parser.parse_bytes_to_protobuf(serialized_bytes)
    assert isinstance(struct_obj, Struct)
    # Quick spot-check of fields
    assert "name" in struct_obj.fields
    assert "nested" in struct_obj.fields


def test_parse_dict_to_bytes(parser, example_dict):
    """
    Test the convenience method that goes (dict -> Protobuf -> bytes).
    """
    raw_bytes = parser.parse_dict_to_bytes(example_dict)
    assert isinstance(raw_bytes, bytes)
    assert len(raw_bytes) > 0


def test_parse_bytes_to_dict(parser, serialized_bytes, example_dict):
    """
    Round-trip check: (bytes -> Protobuf -> dict).
    Compare final dict with original (order, floats vs. ints, etc.
    may differ slightly, but core data should match).
    """
    parsed_dict = parser.parse_bytes_to_dict(serialized_bytes)
    assert isinstance(parsed_dict, dict)
    assert "name" in parsed_dict
    assert parsed_dict["name"] == example_dict["name"]
    assert parsed_dict["count"] == example_dict["count"]

    # Nested structure check
    assert "nested" in parsed_dict
    nested = parsed_dict["nested"]
    assert nested.get("enabled") is True
    assert nested.get("values") == [1, 2, 3]


def test_parse_protobuf_to_bytes_invalid_type(parser):
    """
    parse_protobuf_to_bytes should return None if called with
    an invalid message type.
    """

    class FakeMessage:
        pass

    result = parser.parse_protobuf_to_bytes(FakeMessage())  # Not a Struct
    assert result is None
