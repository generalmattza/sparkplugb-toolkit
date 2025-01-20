EXAMPLE_PAYLOAD_SPARKPLUGB_JSON = {
    "timestamp": 1737090405,
    "metrics": [
        {
            "name": "AXUV_example",
            "timestamp": 1737090405,
            "datatype": 16,
            "properties": {
                "keys": ["gain", "range"],
                "values": [
                    {
                        "type": 21,
                        "propertysets_value": {
                            "propertyset": [
                                {
                                    "keys": ["ch1", "ch2", "ch3", "ch4"],
                                    "values": [
                                        {"type": 3, "int_value": 1000},
                                        {"type": 3, "int_value": 1000},
                                        {"type": 3, "int_value": 1000},
                                        {"type": 3, "int_value": 1000},
                                    ],
                                }
                            ]
                        },
                    },
                    {"type": 3, "int_value": 5},
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
    "body": "UNSTRUCTURED_BINARY_DATA - Used for data that does not fit the structured data model",
}
