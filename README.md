
---

# SparkplugB Toolkit

**A Python library that provides a high-level toolkit for reading, writing, and manipulating SparkplugB payloads using Protobuf.**

## Table of Contents

- [Background](#background)
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Parsing SparkplugB Payloads](#parsing-sparkplugb-payloads)
  - [Working with DataSets](#working-with-datasets)
  - [Metric Properties](#metric-properties)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Background

### What are Protocol Buffers (Protobuf)?

**Protocol Buffers** (often referred to as “Protobuf”) is a language-neutral, platform-neutral, extensible mechanism for serializing structured data. It was originally developed by Google and provides:

- **Compact** binary representation.
- **Strongly typed** schemas.
- **Fast** serialization and deserialization compared to plain text formats like JSON or XML.

Refer to this link for more information on usage, and creating custom schema that can be used by this library.
[https://protobuf.dev/](https://protobuf.dev/)

### SparkplugB

**SparkplugB** is a specification for industrial IoT (IIoT) systems built on top of MQTT. It defines how data points (metrics) and payloads are structured, using **Protobuf** under the hood to handle serialization. The SparkplugB specification ensures consistent data models for various industrial use cases.

---

## Overview

This repository provides the **SparkplugB Toolkit**, a library that offers:

1. A **generic** Protobuf parser base class (`ProtobufParser`), which handles:
   - **bytes** <-> Protobuf message conversion
   - **dict** <-> Protobuf message conversion (through Protobuf’s JSON format)
2. A **specialized** SparkplugB parser class (`SparkplugBParser`) built atop `ProtobufParser` to work with SparkplugB’s `Payload` messages:
   - Extends the base class with SparkplugB-specific methods for creating and reading SparkplugB data structures.
   - Provides convenience utilities for Sparkplug DataSets, metric properties, enumerations, etc.

This **toolkit** aims to simplify interactions with SparkplugB payloads by removing lower-level Protobuf details and providing a user-friendly, Pythonic API.

---

## Features

- **Generic Protobuf Parsing**: Use `ProtobufParser` for any Protobuf message type.
- **SparkplugB Specialization**: 
  - `SparkplugBParser` specifically targets `sparkplug_b_pb2.Payload`.
  - Utility methods for building “DataSet” metrics and converting them to/from `pandas.DataFrame`.
  - Easy handling of **metric properties** (property sets, property lists).
- **Enumerations and Mappings** for SparkplugB data types (`MetricDataType`, `DataSetDataType`, etc.).
- **Logging & Error Handling** with Python’s built-in `logging`.

---

## Installation

You can install the SparkplugB Toolkit in several ways:

1. **Basic Installation**  
   ```bash
   pip install .
   ```
   or in editable (development) mode:
   ```bash
   pip install --editable .
   ```

2. **If Using UV Package Manager**  
   If you are using uv package manager:
   ```bash
   uv venv
   uv sync
   ```

3. **Development & Testing**  
   If you plan to run the test suite, install the **development** dependencies:
   ```bash
   pip install .[dev]
   ```
   If using uv package manager:
   ```bash
    uv sync --dev
   ```
   This ensures you have all libraries necessary for running tests (like Pytest) and any optional features.

---

## Usage

Below is a brief overview. For detailed information, see the docstrings in `sparkplug_b.py` and `protobuf_parser.py`.

### Parsing SparkplugB Payloads

```python
from sparkplugb_toolkit.sparkplug_b import SparkplugBParser

parser = SparkplugBParser()

# Convert raw bytes to a SparkplugB Payload
with open("some_payload.bin", "rb") as f:
    raw_bytes = f.read()

payload_obj = parser.parse_bytes_to_protobuf(raw_bytes)
print(payload_obj.metrics)  # Inspect SparkplugB metrics, etc.

# Convert a Python dict to a SparkplugB Payload
payload_dict = {
    "timestamp": 1737090405,
    "metrics": [
        {
            "name": "my_metric",
            "datatype": 3,  # e.g., Int32
            "int_value": 42
        }
    ],
}
payload_obj = parser.parse_dict_to_protobuf(payload_dict)

# Convert a Protobuf Payload back to bytes
serialized = parser.parse_protobuf_to_bytes(payload_obj)

# Or back to a dictionary
dict_representation = parser.parse_bytes_to_dict(serialized)
```

### Working with DataSets

SparkplugB DataSets are Protobuf structures that can be turned into **pandas** DataFrames. The toolkit makes this easy:

```python
# parse_datasets_to_dfs returns one or more DataFrames plus any metric properties
df_or_dfs, properties = parser.parse_datasets_to_dfs(payload_obj)

if df_or_dfs is None:
    print("No DataSet metrics found.")
elif isinstance(df_or_dfs, list):
    # Multiple DataSets
    for df, prop in zip(df_or_dfs, properties):
        print("DataFrame:\n", df)
        print("Properties:\n", prop)
else:
    # Single DataSet
    print("Single DataFrame:\n", df_or_dfs)
    print("Properties:\n", properties)
```

Similarly, you can **create** new DataSet metrics:

```python
dataset = parser.init_dataset_metric(
    payload=payload_obj,
    name="example_dataset",
    types=[3, 3, 3],   # e.g. Int32, Int32, Int32
    columns=["col1", "col2", "col3"],
)

parser.add_rows_to_dataset(dataset, [
    [1, 2, 3],
    [4, 5, 6],
])
print(dataset)
>>>
num_of_columns: 3
columns: "1"
columns: "2"
columns: "3"
types: 3
types: 3
types: 3
rows {
  elements {
    int_value: 1
  }
  elements {
    int_value: 2
  }
  elements {
    int_value: 3
  }
}
rows {
  elements {
    int_value: 4
  }
  elements {
    int_value: 5
  }
  elements {
    int_value: 6
  }
}
```

### Metric Properties

Metrics can include nested properties (`propertyset_value`, `propertysets_value`). The parser automatically handles these, translating them into Python dictionaries when converting the Payload to a dict.

---

## Testing

We use **pytest** for testing. Tests typically reside in a `tests/` directory.

Run tests with:

```bash
pytest
```

For more verbose output:

```bash
pytest -v
```

This library uses a combination of:
- **Unit tests** for generic Protobuf parsing in `ProtobufParser`.
- **Integration tests** for SparkplugB-specific features in `SparkplugBParser`.

---

## License

This library is released under the [MIT License](LICENSE). By contributing, you agree that your contributions will be licensed under the same open source license.

---