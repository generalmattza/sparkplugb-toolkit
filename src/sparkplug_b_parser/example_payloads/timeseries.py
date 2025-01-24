# Expanded Time Series Payload Example
import base64


EXAMPLE_PAYLOAD_SPARKPLUGB_TIMESERIES = {
    "timestamp": 1626170000000,  # Payload-level timestamp (ms since epoch)
    "metrics": [
        {
            "name": "temperature",
            "datatype": 9,  # 9 = Float
            "timestamp": 1626170001000,
            "float_value": 23.7,
            "properties": {
                "keys": ["units", "location"],
                "values": [
                    {"type": 12, "string_value": "C"},  # 12 => String
                    {"type": 12, "string_value": "Lab1"},
                ],
            },
        },
        {
            "name": "pressure",
            "datatype": 10,  # 10 = Double
            "timestamp": 1626170001500,
            "float_value": 101.325,
            "properties": {
                "keys": ["units"],
                "values": [{"type": 12, "string_value": "kPa"}],
            },
        },
        {
            "name": "humidity",
            "datatype": 9,  # 9 = Float
            "timestamp": 1626170002000,
            "float_value": 45.2,
            # no properties here
        },
        {
            "name": "vibration",
            "datatype": 10,  # 10 = Double
            "timestamp": 1626170002500,
            "float_value": 0.002,
            "properties": {
                "keys": ["sensor_id", "axis"],
                "values": [
                    {"type": 12, "string_value": "VibSensor45"},
                    {"type": 12, "string_value": "Z"},
                ],
            },
        },
        {
            "name": "alarm",
            "datatype": 11,  # 11 = Boolean
            "timestamp": 1626170003000,
            "boolean_value": True,
            "properties": {
                "keys": ["description"],
                "values": [
                    {"type": 12, "string_value": "High Temperature Alarm"},
                ],
            },
        },
    ],
    "body": base64.b64encode(b"optional raw data here").decode("utf-8"),
}
