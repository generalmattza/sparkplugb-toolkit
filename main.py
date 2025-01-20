from sparkplugb_toolkit import SparkplugBParser


EXAMPLE_TIMESERIES_PAYLOAD = {
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
    ],
}

EXAMPLE_DATASET_PAYLOAD = {
    "timestamp": 1737090405,  # Payload-level timestamp
    "metrics": [
        {
            "name": "AXUV_example",
            "timestamp": 1737090405,  # Optional metric-level timestamp
            "datatype": 16,  # 16 -> DataSet
            "properties": {
                "keys": ["gain", "range"],  # repeated string
                "values": [
                    {
                        "type": 21,  # 21 -> PropertySetList
                        "propertysets_value": {
                            "propertyset": [
                                {
                                    "keys": ["ch1", "ch2", "ch3", "ch4"],
                                    "values": [
                                        {"type": 3, "int_value": 1000},  # e.g., int32
                                        {"type": 3, "int_value": 1000},
                                        {"type": 3, "int_value": 1000},
                                        {"type": 3, "int_value": 1000},
                                    ],
                                }
                            ]
                        },
                    },
                    {
                        "type": 3,  # 3 -> int32
                        "int_value": 5,
                    },
                ],
            },
            "dataset_value": {
                "num_of_columns": 5,
                "columns": ["idx", "ch1", "ch2", "ch3", "ch4"],
                "types": [3, 2, 2, 2, 2],
                "rows": [
                    {
                        "elements": [
                            {"int_value": 0},
                            {"int_value": 1},
                            {"int_value": 2},
                            {"int_value": 3},
                            {"int_value": 4},
                        ]
                    },
                    {
                        "elements": [
                            {"int_value": 1},
                            {"int_value": 2},
                            {"int_value": 3},
                            {"int_value": 4},
                            {"int_value": 5},
                        ]
                    },
                    {
                        "elements": [
                            {"int_value": 2},
                            {"int_value": 3},
                            {"int_value": 4},
                            {"int_value": 5},
                            {"int_value": 6},
                        ]
                    },
                ],
            },
        }
    ],
    # The “body” field is a bytes field in Protobuf;
    # here, it is shown as a string for demonstration.
    "body": b"UNSTRUCTURED_BINARY_DATA - Used for data that does not fit the structured data model",
}

if __name__ == "__main__":
    parser = SparkplugBParser()

    # Parse SparkplugB payload containing timeseries data
    payload = parser.parse_dict_to_protobuf(EXAMPLE_TIMESERIES_PAYLOAD)
    print(payload)
    print(payload.SerializeToString())
    print(parser.parse_protobuf_to_dict(payload))

    # Parse SparkplugB payload containing a dataset
    payload = parser.parse_dict_to_protobuf(EXAMPLE_DATASET_PAYLOAD)
    print(payload)
    print(payload.SerializeToString())
    print(parser.parse_protobuf_to_dict(payload))
    # Extract dataset from the payload
    df, properties = parser.parse_datasets_to_dfs(payload)
    print(df)
    print(properties)
