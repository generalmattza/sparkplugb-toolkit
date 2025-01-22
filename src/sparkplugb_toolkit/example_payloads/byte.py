EXAMPLE_PAYLOAD_SPARKPLUGB_BYTES = {
    "timestamp": "1737406558",  # Message sending time
    "metrics": [
        {
            "name": "AXUV1_ch1",
            "timestamp": "1737406554",  # Data acquisition time
            "datatype": 17,  # Bytes type
            "properties": {
                "keys": [
                    "channel_id",  # int32; (0: ch1, 1: ch2, 2: ch3, 3: ch4)
                    "ch_gain",  # float32
                    "ch_range",  # float32
                    "ch_offset",  # float32
                    "wave_byte_order",  # int32; (0: big-endian, 1: little-endian)
                    "time_zero",  # float32
                    "time_range",  # float32
                    "acq_srate",  # int32
                    "acq_bit_res",  # int32
                    "acq_total_samples",  # int32
                ],
                "values": [
                    {"type": 3, "int_value": 0},
                    {"type": 9, "float_value": 1000.0},
                    {"type": 9, "float_value": 5.0},  # e.g., int32
                    {"type": 9, "float_value": 0.0},
                    {"type": 3, "int_value": 0},
                    {"type": 9, "float_value": 0.0},
                    {"type": 9, "float_value": 0.032764},
                    {"type": 3, "int_value": 250000},
                    {"type": 3, "int_value": 16},
                    {"type": 3, "int_value": 8191},
                ],
            },
            "bytes_value": b"bytes_data_here",
        },
        {
            "name": "AXUV1_ch2",
            "timestamp": "1737406554",  # Data acquisition time
            "datatype": 17,  # Bytes type
            "properties": {
                "keys": [
                    "channel_id",  # int32; (0: ch1, 1: ch2, 2: ch3, 3: ch4)
                    "ch_gain",  # float32
                    "ch_range",  # float32
                    "ch_offset",  # float32
                    "wave_byte_order",  # int32; (0: big-endian, 1: little-endian)
                    "time_zero",  # float32
                    "time_range",  # float32
                    "acq_srate",  # int32
                    "acq_bit_res",  # int32
                    "acq_total_samples",  # int32
                ],
                "values": [
                    {"type": 3, "int_value": 1},
                    {"type": 9, "float_value": 1000.0},
                    {"type": 9, "float_value": 5.0},  # e.g., int32
                    {"type": 9, "float_value": 0.0},
                    {"type": 3, "int_value": 0},
                    {"type": 9, "float_value": 0.0},
                    {"type": 9, "float_value": 0.032764},
                    {"type": 3, "int_value": 250000},
                    {"type": 3, "int_value": 16},
                    {"type": 3, "int_value": 8191},
                ],
            },
            "bytes_value": b"bytes_data_here",
        },
    ],
}
