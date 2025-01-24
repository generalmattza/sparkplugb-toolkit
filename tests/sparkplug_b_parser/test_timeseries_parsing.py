import pytest


def test_parse_timeseries_payload(example_message_timeseries, parser):
    # Ensure that the dataset is parsed correctly
    payload = parser.parse_bytes_to_protobuf(example_message_timeseries)
    assert payload.metrics[0].name == "temperature"
    assert payload.metrics[0].datatype == 9
    assert payload.metrics[0].float_value == pytest.approx(23.7)
    assert payload.metrics[0].properties.keys == ["units", "location"]
    assert payload.metrics[0].properties.values[0].type == 12
    assert payload.metrics[0].properties.values[0].string_value == "C"
    assert payload.metrics[0].properties.values[1].type == 12
    assert payload.metrics[0].properties.values[1].string_value == "Lab1"

    assert payload.metrics[1].name == "pressure"
    assert payload.metrics[1].datatype == 10
    assert payload.metrics[1].float_value == pytest.approx(101.325)
    assert payload.metrics[1].properties.keys == ["units"]
    assert payload.metrics[1].properties.values[0].type == 12
    assert payload.metrics[1].properties.values[0].string_value == "kPa"

    assert payload.metrics[2].name == "humidity"
    assert payload.metrics[2].datatype == 9
    assert payload.metrics[2].float_value == pytest.approx(45.2)
    assert payload.metrics[2].properties.keys == []
    assert payload.metrics[2].properties.values == []

    assert payload.metrics[3].name == "vibration"
    assert payload.metrics[3].datatype == 10
    assert payload.metrics[3].float_value == pytest.approx(0.002)
    assert payload.metrics[3].properties.keys == ["sensor_id", "axis"]
    assert payload.metrics[3].properties.values[0].type == 12
    assert payload.metrics[3].properties.values[0].string_value == "VibSensor45"
    assert payload.metrics[3].properties.values[1].type == 12
    assert payload.metrics[3].properties.values[1].string_value == "Z"

    assert payload.metrics[4].name == "alarm"
    assert payload.metrics[4].datatype == 11
    assert payload.metrics[4].boolean_value == True
    assert payload.metrics[4].properties.keys == ["description"]
    assert payload.metrics[4].properties.values[0].type == 12
    assert (
        payload.metrics[4].properties.values[0].string_value == "High Temperature Alarm"
    )
    # Ensure that the body is parsed correctly
    assert payload.body == b"optional raw data here"
