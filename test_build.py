from sparkplug_b import Payload
from tahu_python_helper import (
    MetricDataType,
    ParameterDataType,
    DataSetDataType,
    addMetric,
    AliasMap,
    initDatasetMetric,
    initTemplateMetric,
)

from sparkplug_b import build_protobuf, build_payload


def example_dataset():

    # Create the node birth payload
    payload = Payload()

    # Add some regular node metrics
    addMetric(
        payload,
        "Node Metric0",
        None,
        MetricDataType.String,
        "hello node",
    )
    addMetric(payload, "Node Metric1", None, MetricDataType.Boolean, True)

    # Create a DataSet (012 - 345) two rows with Int8, Int16, and Int32 contents and headers Int8s, Int16s, Int32s and add it to the payload
    columns = ["Int8s", "Int16s", "Int32s"]
    types = [DataSetDataType.Int8, DataSetDataType.Int16, DataSetDataType.Int32]
    dataset = initDatasetMetric(payload, "DataSet", AliasMap.Dataset, columns, types)
    row = dataset.rows.add()
    element = row.elements.add()
    element.int_value = 0
    element = row.elements.add()
    element.int_value = 1
    element = row.elements.add()
    element.int_value = 2
    row = dataset.rows.add()
    element = row.elements.add()
    element.int_value = 3
    element = row.elements.add()
    element.int_value = 4
    element = row.elements.add()
    element.int_value = 5

    # Add a metric with a custom property
    metric = addMetric(
        payload, "Node Metric2", AliasMap.Node_Metric2, MetricDataType.Int16, 13
    )
    metric.properties.keys.extend(["engUnit"])
    propertyValue = metric.properties.values.add()
    propertyValue.type = ParameterDataType.String
    propertyValue.string_value = "MyCustomUnits"

    # Create the UDT definition value which includes two UDT members and a single parameter and add it to the payload
    template = initTemplateMetric(
        payload, "_types_/Custom_Motor", None, None
    )  # No alias for Template definitions
    templateParameter = template.parameters.add()
    templateParameter.name = "Index"
    templateParameter.type = ParameterDataType.String
    templateParameter.string_value = "0"
    addMetric(
        template, "RPMs", None, MetricDataType.Int32, 0
    )  # No alias in UDT members
    addMetric(
        template, "AMPs", None, MetricDataType.Int32, 0
    )  # No alias in UDT members

    # Publish the node birth certificate
    # payload = payload.SerializeToString()
    payload_obj = build_payload(payload)

    protobuf_obj = build_protobuf(payload_obj)

    print(payload_obj)
    print(protobuf_obj)

    print("here")


if __name__ == "__main__":
    example_dataset()
