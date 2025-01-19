import logging
import pandas as pd
import time
from itertools import zip_longest  # Potentially useful if column lengths differ

import sparkplug_b.python.sparkplug_b_pb2 as sparkplug_b_pb2
from google.protobuf.json_format import ParseDict, MessageToDict
from google.protobuf.message import DecodeError

logger = logging.getLogger(__name__)


class AliasMap:
    """Commonly used aliases for Sparkplug metrics."""

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
    """Enumeration for Sparkplug DataSet column types."""

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


class ParameterDataType:
    """Enumeration for Template Parameter data types."""

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
    """
    Enumeration for Sparkplug Metrics.
    Note: If you have repeated this class, consider consolidating into one definition.
    """

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


# Maps the integer data type (MetricDataType.*) to the oneof field name in the Protobuf.
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

# Maps integer data type (MetricDataType.*) to the corresponding Python type
# used when converting from Protobuf to DataFrame.
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
    MetricDataType.DataSet: None,  # or a custom type if needed
    MetricDataType.Bytes: bytes,
    MetricDataType.File: bytes,
    MetricDataType.Template: None,  # or handle specially
}


def parse_message_to_protobuf(message: bytearray) -> sparkplug_b_pb2.Payload:
    """
    Deserialize raw bytes (in a bytearray) into a SparkplugB Payload.

    Args:
        message (bytearray): The raw message bytes representing a serialized Payload.

    Returns:
        sparkplug_b_pb2.Payload: The deserialized Payload object.
    """
    logger.debug("Parsing message to Protobuf Payload.")
    payload = sparkplug_b_pb2.Payload()
    try:
        payload.ParseFromString(message)
        logger.debug("Successfully parsed message into Payload.")
    except DecodeError as e:
        logger.error(f"Error decoding payload: {e}", exc_info=True)
    return payload


def parse_dict_to_protobuf(packet: dict) -> sparkplug_b_pb2.Payload:
    """
    Convert a Python dictionary (structured like JSON) into a SparkplugB Payload.

    Args:
        packet (dict): The dictionary containing Payload fields.

    Returns:
        sparkplug_b_pb2.Payload: The populated Protobuf Payload.
    """
    logger.debug("Converting dictionary to Protobuf Payload.")
    payload = sparkplug_b_pb2.Payload()
    ParseDict(packet, payload)
    logger.debug("Dictionary successfully converted to Payload.")
    return payload


def parse_message_to_dict(message: bytes) -> dict:
    """
    Deserialize a Protobuf Payload and convert it to a Python dictionary.

    Args:
        message (bytes): Serialized Protobuf message bytes.

    Returns:
        dict: The deserialized Payload in dictionary form.
    """
    logger.debug("Parsing message bytes into dictionary.")
    # Create a temporary Payload object
    payload = sparkplug_b_pb2.Payload()
    try:
        payload.ParseFromString(message)
    except DecodeError as e:
        logger.error(f"Error decoding payload: {e}", exc_info=True)
        return {}
    packet = MessageToDict(
        payload,
        preserving_proto_field_name=True,
        use_integers_for_enums=False,
        float_precision=None,
    )
    logger.debug("Successfully parsed message into dictionary.")
    return packet


def parse_protobuf_to_message(protobuf: sparkplug_b_pb2.Payload) -> bytes:
    """
    Serialize a SparkplugB Payload into raw bytes.

    Args:
        protobuf (sparkplug_b_pb2.Payload): The Payload to serialize.

    Returns:
        bytes: The serialized byte string of the Protobuf Payload.
    """
    logger.debug("Serializing Protobuf Payload to bytes.")
    try:
        message = protobuf.SerializeToString()
        logger.debug("Successfully serialized Payload to bytes.")
        return message
    except Exception as e:
        logger.error(f"Error serializing payload: {e}", exc_info=True)
        return b""


def parse_payload_to_dfs(
    payload: sparkplug_b_pb2.Payload,
) -> pd.DataFrame | list[pd.DataFrame]:
    """
    Extract one or more DataSets from a SparkplugB Payload and convert them to pandas DataFrames.

    This function assumes that the Payload contains at least one metric of datatype = DataSet.

    Args:
        payload (sparkplug_b_pb2.Payload): A SparkplugB Payload object containing one or more DataSets.

    Returns:
        pd.DataFrame | list[pd.DataFrame]:
            - A single DataFrame if only one DataSet is found in the Payload.
            - A list of DataFrames if multiple DataSets are found.
    """
    logger.debug("Converting Payload to DataFrames.")
    assert isinstance(payload, sparkplug_b_pb2.Payload)

    # Gather all DataSet metrics
    datasets = [
        m.dataset_value for m in payload.metrics if m.datatype == MetricDataType.DataSet
    ]
    if not datasets:
        logger.warning("No DataSet metrics found in the Payload.")
        return []

    dfs = []
    for dataset in datasets:
        # Check columns and types
        if len(dataset.columns) != len(dataset.types):
            msg = "Columns and types mismatch in DataSet."
            logger.error(msg)
            raise ValueError(msg)

        # Pre-compute the Protobuf field names and Python types for each column
        field_names = [metric_value_field_map.get(t) for t in dataset.types]
        py_types = [metric_python_type_map.get(t) for t in dataset.types]

        # Build the data matrix via list comprehension
        data = [
            [
                # Convert each element to the correct Python type
                py_type(getattr(element, field_name))
                for element, field_name, py_type in zip(
                    row.elements, field_names, py_types
                )
            ]
            for row in dataset.rows
        ]

        # Create the DataFrame
        columns = [str(col) for col in dataset.columns]
        df = pd.DataFrame(data, columns=columns)

        logger.info(
            f"Extracted DataFrame from payload with shape {df.shape}",
            extra={
                "shape": df.shape,
                # The next attributes are not standard in DataSet, but if you had them:
                # "name": getattr(dataset, "name", None),
                # "alias": getattr(dataset, "alias", None),
                # "timestamp": getattr(dataset, "timestamp", None),
            },
        )
        dfs.append(df)

    # Return a single DataFrame if there's only one
    logger.debug(f"Returning {len(dfs)} DataFrame(s) from the payload.")
    if len(dfs) == 1:
        return dfs[0]
    return dfs


def init_dataset_metric(
    payload: sparkplug_b_pb2.Payload,
    name: str | None,
    types: list[int],
    columns: list[str],
    timestamp: int | None = None,
    alias: int | None = None,
) -> sparkplug_b_pb2.Payload.DataSet:
    """
    Initialize a new metric in the given Payload with DataSet type.

    Args:
        payload (sparkplug_b_pb2.Payload): The Payload to which the DataSet metric will be added.
        name (str | None): The name of the new metric (optional).
        types (list[int]): A list of integer codes (MetricDataType.*) for each column.
        columns (list[str]): Column names matching `types`.
        timestamp (int | None, optional): Timestamp in ms. Defaults to current time.
        alias (int | None, optional): Alias for the metric. Defaults to None.

    Returns:
        sparkplug_b_pb2.Payload.DataSet: The newly created DataSet object within the metric.
    """
    logger.debug("Initializing a DataSet metric in the Payload.")
    metric = payload.metrics.add()
    if name is not None:
        metric.name = name
    if alias is not None:
        metric.alias = alias
    metric.timestamp = timestamp or int(round(time.time() * 1000))
    metric.datatype = MetricDataType.DataSet

    # Set up the dataset
    dataset = metric.dataset_value
    dataset.num_of_columns = len(types)
    dataset.columns.extend(columns)
    dataset.types.extend(types)
    logger.debug(
        f"Initialized DataSet metric: name={name}, alias={alias}, "
        f"timestamp={metric.timestamp}, #columns={len(columns)}"
    )
    return dataset


def add_rows_to_dataset(
    dataset: sparkplug_b_pb2.Payload.DataSet, rows: list[list[int | float | str]]
) -> sparkplug_b_pb2.Payload.DataSet:
    """
    Add rows of data to an existing DataSet object. Each row is a list of values
    that correspond to the column types in dataset.types.

    Args:
        dataset (sparkplug_b_pb2.Payload.DataSet): The DataSet to which rows will be added.
        rows (list[list[int|float|str]]): A list of rows. Each row is a list of values matching
            the column types in dataset.types.

    Returns:
        sparkplug_b_pb2.Payload.DataSet: The updated DataSet with new rows appended.
    """
    logger.debug("Adding rows to DataSet.")
    for row_index, row in enumerate(rows):
        row_pb = dataset.rows.add()  # Add a new Row message
        for col_index, (value, type_code) in enumerate(zip(row, dataset.types)):
            element_pb = row_pb.elements.add()

            # Map type code to the correct oneof field name
            field_name = metric_value_field_map.get(type_code)
            if not field_name:
                msg = f"Unsupported data type: {type_code}"
                logger.error(msg)
                raise ValueError(msg)

            # Assign the value
            setattr(element_pb, field_name, value)
        logger.debug(f"Added row {row_index} with {len(row)} element(s).")

    logger.debug(f"Total rows in dataset after addition: {len(dataset.rows)}.")
    return dataset
