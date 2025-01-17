from enum import IntEnum
from typing import List, Optional, Union, Any, ForwardRef
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationInfo
import pandas as pd

# Reference ChatGPT chat: https://chatgpt.com/share/6789edde-aeac-8007-942b-116c1fde9ae6
# Refer to https://sparkplug.eclipse.org/specification/version/3.0/documents/sparkplug-specification-3.0.0.pdf


#
# 1) Sparkplug 3.0 DataType codes (0–24).
#
class DataType(IntEnum):
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
    PropertySet = 20
    PropertySetList = 21
    Int128 = 22
    UInt128 = 23
    XML = 24


#
# 2) DataSet Models
#
class DataSetRow(BaseModel):
    """
    Each row contains 'elements' that match the columns/types count.
    """

    elements: List[Any] = Field(..., description="Row data elements")


class DataSetPayload(BaseModel):
    """
    Matches the Sparkplug layout for dataType=16 (DataSet).
    One array for column names, another array for column types,
    and an array of rows.
    """

    num_of_columns: int
    columns: List[str]
    types: List[int]  # each int is a Sparkplug data-type code
    rows: List[DataSetRow]

    @model_validator(mode="after")
    def check_consistency(self):
        """
        Validate after all fields are parsed, ensuring
        columns and types match num_of_columns, and each row has
        the correct number of elements.
        """
        # Check columns length
        if len(self.columns) != self.num_of_columns:
            raise ValueError(
                f"columns length ({len(self.columns)}) "
                f"must match num_of_columns={self.num_of_columns}."
            )
        # Check types length
        if len(self.types) != self.num_of_columns:
            raise ValueError(
                f"types length ({len(self.types)}) "
                f"must match num_of_columns={self.num_of_columns}."
            )
        # Check each row
        for idx, row in enumerate(self.rows):
            if len(row.elements) != self.num_of_columns:
                raise ValueError(
                    f"Row {idx} has {len(row.elements)} elements, "
                    f"but num_of_columns={self.num_of_columns}."
                )
        return self

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the DataSetPayload into a Pandas DataFrame.
        Attempts to map Sparkplug data types to Pandas/Numpy dtypes
        where possible.
        """
        # Create a DataFrame from rows
        df = pd.DataFrame(data=[r.elements for r in self.rows], columns=self.columns)

        # Optionally map Sparkplug data types (self.types) to Pandas dtypes
        sp_type_to_pd = {
            DataType.Int8: "Int8",
            DataType.Int16: "Int16",
            DataType.Int32: "Int32",
            DataType.Int64: "Int64",
            DataType.UInt8: "UInt8",
            DataType.UInt16: "UInt16",
            DataType.UInt32: "UInt32",
            DataType.UInt64: "UInt64",
            DataType.Float: "float32",
            DataType.Double: "float64",
            DataType.Boolean: "boolean",  # Pandas nullable Boolean
            # If you like, you can add others or refine as needed
        }

        # Cast each column based on self.types
        for col_idx, sp_type_code in enumerate(self.types):
            col_name = self.columns[col_idx]
            sp_type_enum = DataType(sp_type_code)
            target_dtype = sp_type_to_pd.get(sp_type_enum)
            if target_dtype:
                try:
                    df[col_name] = df[col_name].astype(target_dtype)
                except ValueError:
                    # If cast fails (e.g., invalid data), skip or raise
                    raise ValueError(
                        f"Failed to cast column '{col_name}' to dtype={target_dtype}"
                    )

        return df


#
# 3) Property Models
#
# We'll define:
#  - PropertySet       => (keys[], values[])
#  - PropertySetList   => (propertySets[])
#  - PropertyValue     => (type, value)
#
# Because PropertyValue can reference PropertySetList, and
# PropertySetList references PropertySet, we have potential recursion.
# We'll use ForwardRef to handle that.

PropertySetRef = ForwardRef("PropertySet")
PropertySetListRef = ForwardRef("PropertySetList")


class PropertySet(BaseModel):
    """
    A Sparkplug property set => (keys[], values[]).
    The length of keys must match the length of values.
    Each item in values is a PropertyValue => (type, value).
    """

    keys: List[str]
    values: List["PropertyValue"]  # ForwardRef to PropertyValue

    @model_validator(mode="after")
    def check_key_value_length(self):
        if len(self.keys) != len(self.values):
            raise ValueError(
                f"Length mismatch: {len(self.keys)} keys "
                f"vs {len(self.values)} values."
            )
        return self


class PropertySetList(BaseModel):
    """
    If dataType=21 => a PropertySetList,
    which is an object with `propertySets[]` (array of PropertySet).
    """

    propertySets: List[PropertySetRef] = Field(default_factory=list)  # type: ignore


class PropertyValue(BaseModel):
    """
    Sparkplug property value => (type, value).
    If type=21 => 'value' is a PropertySetList,
    which your JSON might provide as a bare array or a dict.
    """

    type: DataType
    value: Union[int, float, bool, str, None, PropertySetList] = None

    @field_validator("value", mode="before")
    def parse_if_propertysetlist(cls, v, info: ValidationInfo):
        from pydantic import ValidationError

        if info.data.get("type") == DataType.PropertySetList:
            # If it's already an object { "propertySets": [...] }
            if isinstance(v, dict):
                return PropertySetList(**v)

            # If it's a bare array [ ... ], parse each item as a PropertySet
            if isinstance(v, list):
                property_sets = []
                for idx, item in enumerate(v):
                    try:
                        property_sets.append(PropertySet(**item))
                    except ValidationError as exc:
                        raise ValueError(
                            f"Error parsing item {idx} in bare array for PropertySetList: {exc}"
                        )
                return PropertySetList(propertySets=property_sets)

        return v


# Now that we have the classes defined, update forward refs
PropertySet.model_rebuild()
PropertySetList.model_rebuild()
PropertyValue.model_rebuild()


#
# 4) Metric Model
#
class Metric(BaseModel):
    name: str
    dataType: DataType  # integer code per Sparkplug table
    # 'properties' => a top-level PropertySet (optional)
    properties: Optional[PropertySet] = None
    # 'value' => if dataType=16 (DataSet), parse as DataSetPayload
    value: Optional[Any] = None

    @field_validator("value", mode="before")
    def coerce_dataset_if_type_16(cls, v, info: ValidationInfo):
        dt = info.data.get("dataType")
        if dt == DataType.DataSet and isinstance(v, dict):
            return DataSetPayload(**v)
        return v


#
# 5) Top-level Sparkplug Payload
#
class SparkplugBPayload(BaseModel):
    timestamp: int
    metrics: List[Metric]
    body: Optional[bytes] = None  # or str, depending on how you store it

    @model_validator(mode="after")
    def check_metrics_nonempty(self):
        if not self.metrics:
            raise ValueError("Must have at least one metric.")
        return self
