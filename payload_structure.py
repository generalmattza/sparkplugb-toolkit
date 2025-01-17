# Refer to https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf


dataset_payload = {
    "timestamp": 1626170000000,
    "metrics": [
        {
            "name": "AXUV_example",
            "dataType": 16,  # 16 is the data type for DataSet
            # "metadata": {
            #     # See section 6.4.7
            # },
            "properties": {
                "keys": ["gain", "range"],  # Array[strings]
                "values": [
                    {
                        "type": 21,  # PropertySetList
                        "value": [
                            {
                                "keys": ["ch1", "ch2", "ch3", "ch4"],  # Array[string]
                                "values": [
                                    {"type": 3, "value": 1000},
                                    {"type": 3, "value": 1000},
                                    {"type": 3, "value": 1000},
                                    {"type": 3, "value": 1000},
                                ],  # Array[PropertyValue]
                            },  # PropertySet
                            {"type": 3, "value": 5},  # PropertyValue
                        ],  # Array[PropertyValue]
                    },  # PropertySet
                ],
            },
            "value": {
                "num_of_columns": 5,
                "columns": ["idx", "ch1", "ch2", "ch3", "ch4"],
                "types": [3, 2, 2, 2, 2],  # uint32, int16, int16, int16, int16
                "rows": [
                    {"elements": [0, 1, 2, 3, 4]},
                    {"elements": [1, 2, 3, 4, 5]},
                    {"elements": [2, 3, 4, 5, 6]},
                ],
            },
        },
    ],
    "body": b"45321753782615381",  # [Optional]
}
