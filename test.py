from sparkplug_b import build_protobuf, build_payload


dataset_payload = {
    "timestamp": 1737090405,
    "metrics": [
        {
            "name": "AXUV_example",
            "datatype": 16,  # 16 is the data type for DataSet
            # "metadata": {
            #     # See section 6.4.7
            # },
            "properties": {
                "keys": [
                    "gain_1",
                    "gain_2",
                    "gain_3",
                    "gain_4",
                    "range_1",
                    "range_2",
                    "range_3",
                    "range_4",
                ],  # Array[strings]
                "values": [
                    {"type": 3, "int_value": 1000},
                    {"type": 3, "int_value": 1000},
                    {"type": 3, "int_value": 1000},
                    {"type": 3, "int_value": 1000},
                    {"type": 3, "int_value": 5},
                    {"type": 3, "int_value": 5},
                    {"type": 3, "int_value": 5},
                    {"type": 3, "int_value": 5},
                ],
            },
            "datasetValue": {
                "num_of_columns": 5,
                "columns": ["idx", "ch1", "ch2", "ch3", "ch4"],
                "types": [3, 2, 2, 2, 2],  # uint32, int16, int16, int16, int16
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
                            {"int_value": 6},
                            {"int_value": 7},
                            {"int_value": 8},
                            {"int_value": 9},
                        ]
                    },
                ],
            },
        },
    ],
    "body": b"UNSTRUCTURED_BINARY_DATA",  # [Optional]
}


# dataset_payload = {
#     "timestamp": 1737090405,
#     "metrics": [
#         {
#             "name": "AXUV_example",
#             "datatype": 16,  # 16 is the data type for DataSet
#             # "metadata": {
#             #     # See section 6.4.7
#             # },
#             "properties": {
#                 "keys": ["gain", "range"],  # Array[strings]
#                 "values": [
#                     {
#                         "type": 21,  # PropertySetList
#                         "propertysets_value": [
#                             {  # First PropertySet
#                                 "keys": ["ch1", "ch2", "ch3", "ch4"],  # Property keys
#                                 "values": [  # Corresponding PropertyValue list
#                                     {"type": 3, "int_value": 1000},
#                                     {"type": 3, "int_value": 1000},
#                                     {"type": 3, "int_value": 1000},
#                                     {"type": 3, "int_value": 1000},
#                                 ],
#                             },
#                         ],
#                     },  # PropertySet
#                     {"type": 3, "int_value": 5},  # PropertyValue
#                 ],
#             },
#             "value": {
#                 "num_of_columns": 5,
#                 "columns": ["idx", "ch1", "ch2", "ch3", "ch4"],
#                 "types": [3, 2, 2, 2, 2],  # uint32, int16, int16, int16, int16
#                 "rows": [
#                     {"elements": [0, 1, 2, 3, 4]},
#                     {"elements": [1, 2, 3, 4, 5]},
#                     {"elements": [2, 3, 4, 5, 6]},
#                 ],
#             },
#         },
#     ],
#     "body": b"UNSTRUCTURED_BINARY_DATA",  # [Optional]
# }


protobuf = build_protobuf(dataset_payload)

print(protobuf)
