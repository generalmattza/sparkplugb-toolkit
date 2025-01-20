# Refer to https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf

EXAMPLE_PAYLOAD_SPARKPLUGB_DATASET = {
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
