import logging
import pandas as pd
import time

import sparkplug_b.python.sparkplug_b_pb2 as sparkplug_b_pb2
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import DecodeError, EncodeError

logger = logging.getLogger(__name__)


class AliasMap:
    Next_Server = 0
    Rebirth = 1
    Reboot = 2
    Dataset = 3
    Node_Metric0 = 4
    Node_Metric1 = 5
    Node_Metric2 = 6
    Node_Metric3 = 7
    Device_Metric0 = 8
    Device_Metric1 = 9
    Device_Metric2 = 10
    Device_Metric3 = 11
    My_Custom_Motor = 12


class DataSetDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14


class MetricDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14
    UUID = 15
    DataSet = 16
    Bytes = 17
    File = 18
    Template = 19


class ParameterDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14


class MetricDataType:
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14
    UUID = 15
    DataSet = 16
    Bytes = 17
    File = 18
    Template = 19


# Maps the integer data type to the *oneof field name* in the Protobuf
metric_value_field_map = {
    MetricDataType.Int8: "int_value",
    MetricDataType.Int16: "int_value",
    MetricDataType.Int32: "int_value",
    MetricDataType.Int64: "long_value",
    MetricDataType.UInt8: "int_value",
    MetricDataType.UInt16: "int_value",
    MetricDataType.UInt32: "int_value",
    MetricDataType.UInt64: "long_value",
    MetricDataType.Float: "float_value",
    MetricDataType.Double: "double_value",
    MetricDataType.Boolean: "boolean_value",
    MetricDataType.String: "string_value",
    MetricDataType.DateTime: "long_value",  # or handle specially
    MetricDataType.Text: "string_value",
    MetricDataType.UUID: "string_value",
    MetricDataType.DataSet: "dataset_value",
    MetricDataType.Bytes: "bytes_value",
    MetricDataType.File: "bytes_value",  # or handle specially
    MetricDataType.Template: "template_value",
}

metric_python_type_map = {
    MetricDataType.Int8: int,
    MetricDataType.Int16: int,
    MetricDataType.Int32: int,
    MetricDataType.Int64: int,
    MetricDataType.UInt8: int,
    MetricDataType.UInt16: int,
    MetricDataType.UInt32: int,
    MetricDataType.UInt64: int,
    MetricDataType.Float: float,
    MetricDataType.Double: float,
    MetricDataType.Boolean: bool,
    MetricDataType.String: str,
    MetricDataType.DateTime: int,
    MetricDataType.Text: str,
    MetricDataType.UUID: str,
    MetricDataType.DataSet: None,
    MetricDataType.Bytes: bytes,
    MetricDataType.File: bytes,
    MetricDataType.Template: None,
}


def parse_message_to_protobuf(message: bytearray) -> sparkplug_b_pb2.Payload:
    # Parse serialized payload data from message
    payload = sparkplug_b_pb2.Payload()
    try:
        payload.ParseFromString(message)
    except DecodeError as e:
        print(f"Error decoding payload: {e}")
    return payload


def parse_dict_to_protobuf(packet: dict) -> sparkplug_b_pb2.Payload:
    # Create a new payload
    payload = sparkplug_b_pb2.Payload()
    # Parse the dictionary into the payload
    ParseDict(packet, payload)
    return payload


def parse_message_to_dict(message: bytes) -> dict:
    # Parse the payload into a dictionary
    packet = MessageToDict(
        message,
        preserving_proto_field_name=True,
        use_integers_for_enums=False,
        float_precision=None,
    )
    return packet


def parse_protobuf_to_message(protobuf: sparkplug_b_pb2.Payload) -> bytes:
    # Serialize the payload to a message in bytes
    message = protobuf.SerializeToString()
    message = bytearray(message)
    return message


def parse_payload_to_dfs(
    payload: sparkplug_b_pb2.Payload,
) -> pd.DataFrame | list[pd.DataFrame]:
    # extract datasets from payload
    assert isinstance(payload, sparkplug_b_pb2.Payload)

    datasets = []
    for metric in payload.metrics:
        if metric.datatype == MetricDataType.DataSet:
            datasets.append(metric.dataset_value)

    assert len(datasets) > 0, "No datasets found in payload"

    dfs = []
    for dataset in datasets:

        assert len(dataset.columns) == len(dataset.types), "Columns and types mismatch"

        columns = dataset.columns
        rows = dataset.rows

        data = []
        # Get the field names and Python types for each type code
        field_names = [
            metric_value_field_map.get(type_code, None) for type_code in dataset.types
        ]
        py_types = [
            metric_python_type_map.get(type_code, None) for type_code in dataset.types
        ]
        # Ensure all column names are strings
        columns = [str(column) for column in columns]
        for row in rows:
            values = []
            for element, field_name, py_type in zip(
                row.elements, field_names, py_types
            ):
                values.append(py_type(getattr(element, field_name)))
            data.append(values)

        # Create the DataFrame
        df = pd.DataFrame(data, columns=columns)

        logger.info(
            f"Extracted DataFrame from payload with shape {df.shape}",
            extra={
                "shape": df.shape,
                "name": getattr(dataset, "name", None),
                "alias": getattr(dataset, "alias", None),
                "timestamp": getattr(dataset, "timestamp", None),
            },
        )

        dfs.append(df)

    logger.info(
        f"Returning {len(dfs)} DataFrames from payload",
        extra={"dfs": len(dfs)},
    )

    if len(dfs) == 1:
        return dfs[0]
    return dfs


def init_dataset_metric(payload, name, types, columns, timestamp=None, alias=None):
    metric = payload.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    timestamp = timestamp or int(round(time.time() * 1000))
    metric.timestamp = timestamp
    metric.datatype = MetricDataType.DataSet

    # Set up the dataset
    metric.dataset_value.num_of_columns = len(types)
    metric.dataset_value.columns.extend(columns)
    metric.dataset_value.types.extend(types)
    return metric.dataset_value


def add_rows_to_dataset(dataset, rows: list[list[int | float | str]]):
    # Each element in dataset.types is an integer that matches your MetricDataType or DataSetType
    # For each row in your input, create a new Row in the dataset:
    for row in rows:
        row_pb = dataset.rows.add()  # Add a new Row message
        for value, type_code in zip(row, dataset.types):
            # Add a new element in this row
            element_pb = row_pb.elements.add()

            # Find which Protobuf field name corresponds to this type_code
            field_name = metric_value_field_map.get(type_code, None)
            if not field_name:
                raise ValueError(f"Unsupported data type: {type_code}")

            # Now set the correct Protobuf field
            setattr(element_pb, field_name, value)

    return dataset
