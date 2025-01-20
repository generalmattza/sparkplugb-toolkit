import logging
import time
from typing import Optional, Tuple, List, Union

import pandas as pd

import sparkplugb_toolkit.sparkplug_b_pb2 as sparkplug_b_pb2
from protobuf_facade import ProtobufParser

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Enums & Constants
# --------------------------------------------------------------------------


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
    Custom0 = 12


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


# Maps from Sparkplug metric data type -> Protobuf oneof field name
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
    MetricDataType.DateTime: "long_value",
    MetricDataType.Text: "string_value",
    MetricDataType.UUID: "string_value",
    MetricDataType.DataSet: "dataset_value",
    MetricDataType.Bytes: "bytes_value",
    MetricDataType.File: "bytes_value",
    MetricDataType.Template: "template_value",
}

# Maps from Sparkplug metric data type -> Python type for DataFrame columns
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
    MetricDataType.DateTime: int,  # or a custom converter
    MetricDataType.Text: str,
    MetricDataType.UUID: str,
    MetricDataType.DataSet: None,  # placeholder for nested objects
    MetricDataType.Bytes: bytes,
    MetricDataType.File: bytes,
    MetricDataType.Template: None,
}

# Maps propertyValue.type -> oneof field name for metric properties
property_value_field_map = {
    1: "int_value",
    2: "int_value",
    3: "int_value",
    4: "long_value",
    9: "float_value",
    10: "double_value",
    11: "boolean_value",
    12: "string_value",
    14: "string_value",
    20: "propertyset_value",
    21: "propertysets_value",
}


# --------------------------------------------------------------------------
# SparkplugB Parser Class
# --------------------------------------------------------------------------


class SparkplugBParser(ProtobufParser[sparkplug_b_pb2.Payload]):
    """
    Specialized parser for SparkplugB Payload messages.

    Inherits from ProtobufParser, where `message_type` is set to
    `sparkplug_b_pb2.Payload`. Use the inherited methods for parsing between:
      - bytes <-> Payload (Protobuf object)
      - dict <-> Payload (Protobuf object)
      - bytes <-> dict

    This class adds Sparkplug-specific utilities for handling datasets, metrics,
    and property sets.
    """

    message_type = sparkplug_b_pb2.Payload

    # ----------------------------------------------------------------------
    # SparkplugB-specific DataSet handling
    # ----------------------------------------------------------------------

    def parse_datasets_to_dfs(
        self, payload: sparkplug_b_pb2.Payload
    ) -> Union[Tuple[pd.DataFrame, dict], Tuple[List[pd.DataFrame], List[dict]]]:
        """
        Extract one or more DataSets from a SparkplugB Payload and convert them
        to pandas DataFrames, along with their corresponding metric properties.

        Args:
            payload (sparkplug_b_pb2.Payload): A SparkplugB Payload that may contain
                one or more DataSet metrics.

        Returns:
            A tuple of either:
              (single_df, single_properties_dict)
            or
              (list_of_dfs, list_of_properties_dicts)

            If no DataSet metrics are found, returns (None, None).
        """
        logger.debug("Converting Payload to DataFrames.")
        if not isinstance(payload, sparkplug_b_pb2.Payload):
            raise TypeError("Expected a sparkplug_b_pb2.Payload instance.")

        datasets, properties, metric_indexes = [], [], []
        for idx, metric in enumerate(payload.metrics):
            if metric.datatype == MetricDataType.DataSet:
                datasets.append(metric.dataset_value)
                metric_indexes.append(idx)
                properties.append(self._parse_metric_properties(metric))

        if not datasets:
            logger.warning("No DataSet metrics found in the Payload.")
            return None, None

        dfs = []
        for idx, dataset in zip(metric_indexes, datasets):
            # Check columns and types
            if len(dataset.columns) != len(dataset.types):
                msg = "Mismatch in number of columns vs. types in the DataSet."
                logger.error(msg)
                raise ValueError(msg)

            # Build Python lists for each row
            field_names = [metric_value_field_map.get(t) for t in dataset.types]
            py_types = [metric_python_type_map.get(t) for t in dataset.types]

            data = [
                [
                    # Convert each element to the correct Python type (if not None)
                    (
                        py_type(getattr(element, field_name))
                        if (py_type and field_name and hasattr(element, field_name))
                        else getattr(element, field_name)
                    )
                    for element, field_name, py_type in zip(
                        row.elements, field_names, py_types
                    )
                ]
                for row in dataset.rows
            ]

            # Create the DataFrame
            columns = [str(col) for col in dataset.columns]
            df = pd.DataFrame(data, columns=columns)

            metric = payload.metrics[idx]
            logger.info(
                f"Extracted DataFrame from payload with shape {df.shape}",
                extra={
                    "shape": df.shape,
                    "metric_name": getattr(metric, "name", None),
                    "alias": getattr(metric, "alias", None),
                    "metric_ts": getattr(metric, "timestamp", None),
                },
            )
            dfs.append(df)

        # Return a single DataFrame if there's only one
        logger.debug(f"Returning {len(dfs)} DataFrame(s) from the payload.")
        if len(dfs) == 1:
            return dfs[0], properties[0]
        return dfs, properties

    def init_dataset_metric(
        self,
        payload: sparkplug_b_pb2.Payload,
        name: Optional[str],
        types: list[int],
        columns: list[str],
        timestamp: Optional[int] = None,
        alias: Optional[int] = None,
    ) -> sparkplug_b_pb2.Payload.DataSet:
        """
        Initialize a new metric in the given Payload with DataSet type.

        Args:
            payload (sparkplug_b_pb2.Payload): The Payload to which the DataSet metric will be added.
            name (str | None): Metric name (optional).
            types (list[int]): List of integer codes from MetricDataType.* for each column.
            columns (list[str]): Column names matching `types`.
            timestamp (int | None): Timestamp in milliseconds. Defaults to now.
            alias (int | None): Alias for the metric. Defaults to None.

        Returns:
            sparkplug_b_pb2.Payload.DataSet: The newly created DataSet object in the metric.
        """
        logger.debug("Initializing a DataSet metric in the Payload.")
        metric = payload.metrics.add()
        if name is not None:
            metric.name = name
        if alias is not None:
            metric.alias = alias
        metric.timestamp = timestamp or int(round(time.time() * 1000))
        metric.datatype = MetricDataType.DataSet

        dataset = metric.dataset_value
        dataset.num_of_columns = len(types)
        dataset.columns.extend(columns)
        dataset.types.extend(types)
        logger.debug(
            f"Initialized DataSet metric: name={name}, alias={alias}, "
            f"timestamp={metric.timestamp}, #columns={len(columns)}, #types={types}."
        )
        return dataset

    def add_rows_to_dataset(
        self,
        dataset: sparkplug_b_pb2.Payload.DataSet,
        rows: List[List[Union[int, float, str, bytes]]],
    ) -> sparkplug_b_pb2.Payload.DataSet:
        """
        Append rows of data to an existing DataSet object. Each row is a list of values
        that must match the column types in `dataset.types`.

        Args:
            dataset (sparkplug_b_pb2.Payload.DataSet): The DataSet to which rows are appended.
            rows (List[List[Union[int, float, str, bytes]]]): One or more rows, where each value
                aligns with the DataSet column types.

        Returns:
            sparkplug_b_pb2.Payload.DataSet: The same DataSet, now updated with new rows.
        """
        logger.debug("Adding rows to an existing DataSet.")
        for row_index, row in enumerate(rows):
            row_pb = dataset.rows.add()  # Add a new Row message
            for value, type_code in zip(row, dataset.types):
                element_pb = row_pb.elements.add()
                field_name = metric_value_field_map.get(type_code)
                if not field_name:
                    msg = f"Unsupported data type: {type_code}"
                    logger.error(msg)
                    raise ValueError(msg)
                setattr(element_pb, field_name, value)
            logger.debug(f"Added row {row_index} with {len(row)} element(s).")

        logger.debug(f"DataSet now has {len(dataset.rows)} total row(s).")
        return dataset

    # ----------------------------------------------------------------------
    # SparkplugB-specific Property Parsing
    # ----------------------------------------------------------------------

    def _parse_metric_properties(self, metric: sparkplug_b_pb2.Payload.Metric) -> dict:
        """
        Extract a Python dictionary of key-value pairs from a metric's 'properties' field.
        Returns an empty dict if the metric has no properties.
        """
        if not metric.HasField("properties"):
            return {}
        return self._parse_propertyset(metric.properties)

    def _parse_propertyset(
        self, property_set: sparkplug_b_pb2.Payload.PropertySet
    ) -> dict:
        """
        Recursively parse a PropertySet into a dict of {key: value}.
        """
        result = {}
        for key, prop_val in zip(property_set.keys, property_set.values):
            result[key] = self._parse_propertyvalue(prop_val)
        return result

    def _parse_propertyvalue(
        self, prop_value: sparkplug_b_pb2.Payload.PropertyValue
    ) -> Optional[object]:
        """
        Convert a PropertyValue to the corresponding Python object, handling
        propertyset nesting where necessary.
        """
        if prop_value.is_null:
            return None

        field_name = property_value_field_map.get(prop_value.type, None)
        if not field_name:
            return None

        raw_value = getattr(prop_value, field_name)

        # Nested property sets
        if field_name == "propertyset_value":
            return self._parse_propertyset(raw_value)
        if field_name == "propertysets_value":
            return self._parse_propertysetlist(raw_value)

        # Otherwise, it's a primitive type
        return raw_value

    def _parse_propertysetlist(
        self, property_set_list: sparkplug_b_pb2.Payload.PropertySetList
    ) -> Union[dict, list]:
        """
        Parse a PropertySetList as either a single dict or a list of dicts.
        """
        parsed_list = [
            self._parse_propertyset(ps) for ps in property_set_list.propertyset
        ]
        if len(parsed_list) == 1:
            return parsed_list[0]
        return parsed_list
